# google_drive_repository.py
"""
Repository to handle Google Drive OAuth and image upload.
"""
import json
import logging
import requests
from datetime import datetime
from typing import Tuple
from app.core.config import settings

logger = logging.getLogger(__name__)

GOOGLE_DRIVE_FILES_URL = 'https://www.googleapis.com/drive/v3/files'
GOOGLE_DRIVE_UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
GOOGLE_DRIVE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_DRIVE_FOLDER_ID = settings.GOOGLE_DRIVE_FOLDER_ID
CLIENT_ID = settings.GOOGLE_CLIENT_ID
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
STORED_REFRESH_TOKEN = settings.GOOGLE_REFRESH_TOKEN


class GoogleDriveRepository:

    def exchange_code_for_tokens(self, code: str) -> Tuple[str, str]:
        logger.info("=== TOKEN EXCHANGE DEBUG ===")
        logger.info(f"REDIRECT_URI: {REDIRECT_URI}")
        logger.info(f"Code (first 20 chars): {code[:20]}...")
        data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        logger.info(f"Sending token request to: {GOOGLE_DRIVE_TOKEN_URL}")
        response = requests.post(GOOGLE_DRIVE_TOKEN_URL, data=data)
        logger.info(f"Google response status: {response.status_code}")
        logger.info(f"Google response body: {response.text}")
        response.raise_for_status()
        tokens = response.json()
        return tokens['access_token'], tokens['refresh_token']

    def refresh_access_token(self, refresh_token: str) -> str:
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        response = requests.post(GOOGLE_DRIVE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()['access_token']

    def get_or_create_folder(self, name: str, parent_id: str, access_token: str) -> str:
        headers = {'Authorization': f'Bearer {access_token}'}
        query = (
            f"name='{name}' and mimeType='application/vnd.google-apps.folder' "
            f"and '{parent_id}' in parents and trashed=false"
        )
        resp = requests.get(GOOGLE_DRIVE_FILES_URL, headers=headers, params={'q': query, 'fields': 'files(id,name)'})
        resp.raise_for_status()
        files = resp.json().get('files', [])
        if files:
            logger.info(f"Found existing folder: {name} (id={files[0]['id']})")
            return files[0]['id']

        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id],
        }
        resp = requests.post(
            GOOGLE_DRIVE_FILES_URL,
            headers={**headers, 'Content-Type': 'application/json'},
            data=json.dumps(metadata),
        )
        resp.raise_for_status()
        folder_id = resp.json()['id']
        logger.info(f"Created folder: {name} (id={folder_id})")
        return folder_id

    def upload_image(self, access_token: str, file_path: str, file_name: str, folder_id: str) -> dict:
        metadata = {
            'name': file_name,
            'parents': [folder_id],
        }
        with open(file_path, 'rb') as f:
            files = {
                'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                'file': (file_name, f, 'image/jpeg'),
            }
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(GOOGLE_DRIVE_UPLOAD_URL, headers=headers, files=files)
        response.raise_for_status()
        return response.json()

    def validate_and_upload(self, file_path: str, file_name: str, upload_type: str = 'pickup',
                            driver_name: str = 'Driver', opportunity_id: str = '') -> dict:
        if not STORED_REFRESH_TOKEN:
            raise Exception("GOOGLE_REFRESH_TOKEN is not set. Admin must complete OAuth flow first.")

        logger.info("Refreshing access token...")
        access_token = self.refresh_access_token(STORED_REFRESH_TOKEN)
        logger.info("Access token obtained successfully.")

        today = datetime.now().strftime('%Y-%m-%d')
        safe_driver = driver_name.replace(' ', '_')

        parent_name = (
            f"Opp{opportunity_id}_{safe_driver}_{today}"
            if opportunity_id else
            f"{safe_driver}_{today}"
        )
        logger.info(f"Creating/finding parent folder: {parent_name}")
        parent_id = self.get_or_create_folder(parent_name, GOOGLE_DRIVE_FOLDER_ID, access_token)

        type_label = 'Pickup' if upload_type == 'pickup' else 'Deliver'
        subfolder_name = f"{type_label}_{today}_{safe_driver}"
        logger.info(f"Creating/finding subfolder: {subfolder_name}")
        subfolder_id = self.get_or_create_folder(subfolder_name, parent_id, access_token)

        logger.info(f"Uploading '{file_name}' to folder '{subfolder_name}' (id={subfolder_id})")
        return self.upload_image(access_token, file_path, file_name, subfolder_id)
