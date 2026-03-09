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

GOOGLE_DRIVE_FILES_URL = settings.GOOGLE_DRIVE_FILES_URL
GOOGLE_DRIVE_UPLOAD_URL = settings.GOOGLE_DRIVE_UPLOAD_URL
GOOGLE_DRIVE_TOKEN_URL = settings.GOOGLE_DRIVE_TOKEN_URL


class GoogleDriveRepository:

    def __init__(self):
        """Load config once and create a shared session for token endpoint calls."""
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.refresh_token = settings.GOOGLE_REFRESH_TOKEN
        self.root_folder_id = settings.GOOGLE_DRIVE_FOLDER_ID

        # Shared session for Google token endpoint (no auth header needed)
        self.token_session = requests.Session()

    def _drive_session(self, access_token: str) -> requests.Session:
        """Create a session pre-configured with the Drive authorization header."""
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {access_token}'})
        return session

    def exchange_code_for_tokens(self, code: str) -> Tuple[str, str]:
        """Exchange a one-time OAuth authorization code for access and refresh tokens."""
        logger.info("=== TOKEN EXCHANGE DEBUG ===")
        logger.info(f"REDIRECT_URI: {self.redirect_uri}")
        logger.info(f"Code (first 20 chars): {code[:20]}...")
        try:
            data = {
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'authorization_code',
            }
            logger.info(f"Sending token request to: {GOOGLE_DRIVE_TOKEN_URL}")
            response = self.token_session.post(GOOGLE_DRIVE_TOKEN_URL, data=data)
            logger.info(f"Google response status: {response.status_code}")
            logger.info(f"Google response body: {response.text}")
            response.raise_for_status()
            tokens = response.json()
            return tokens['access_token'], tokens['refresh_token']
        except Exception as e:
            logger.error(f"Failed to exchange authorization code for tokens: {e}", exc_info=True)
            raise

    def refresh_access_token(self, refresh_token: str) -> str:
        """Use the stored refresh token to get a fresh access token from Google."""
        try:
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
            }
            response = self.token_session.post(GOOGLE_DRIVE_TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}", exc_info=True)
            raise

    def get_or_create_folder(self, name: str, parent_id: str, session: requests.Session) -> str:
        """Find a folder by name under parent_id, or create it if it doesn't exist."""
        try:
            query = (
                f"name='{name}' and mimeType='application/vnd.google-apps.folder' "
                f"and '{parent_id}' in parents and trashed=false"
            )
            resp = session.get(GOOGLE_DRIVE_FILES_URL, params={'q': query, 'fields': 'files(id,name)'})
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
            resp = session.post(
                GOOGLE_DRIVE_FILES_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(metadata),
            )
            resp.raise_for_status()
            folder_id = resp.json()['id']
            logger.info(f"Created folder: {name} (id={folder_id})")
            return folder_id
        except Exception as e:
            logger.error(f"Failed to get or create folder '{name}': {e}", exc_info=True)
            raise

    def upload_image(self, session: requests.Session, file_path: str, file_name: str, folder_id: str) -> dict:
        """Upload a single image file into the specified Google Drive folder."""
        try:
            metadata = {
                'name': file_name,
                'parents': [folder_id],
            }
            with open(file_path, 'rb') as f:
                files = {
                    'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                    'file': (file_name, f, 'image/jpeg'),
                }
                response = session.post(GOOGLE_DRIVE_UPLOAD_URL, files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to upload image '{file_name}': {e}", exc_info=True)
            raise

    def validate_and_upload(self, file_path: str, file_name: str, upload_type: str = 'pickup',
                            driver_name: str = 'Driver', opportunity_id: str = '') -> dict:
        """
        Orchestrate the full upload flow:
        1. Refresh access token
        2. Find/create parent folder  (Opp{id}_{driver}_{date})
        3. Find/create subfolder      (Pickup/Deliver_{date}_{driver})
        4. Upload the image into the subfolder
        """
        if not self.refresh_token:
            raise Exception("GOOGLE_REFRESH_TOKEN is not set. Admin must complete OAuth flow first.")

        try:
            logger.info("Refreshing access token...")
            access_token = self.refresh_access_token(self.refresh_token)
            logger.info("Access token obtained successfully.")

            # Single Drive session for all API calls in this upload
            session = self._drive_session(access_token)

            today = datetime.now().strftime('%Y-%m-%d')
            safe_driver = driver_name.replace(' ', '_')

            parent_name = (
                f"Opp{opportunity_id}_{safe_driver}_{today}"
                if opportunity_id else
                f"{safe_driver}_{today}"
            )
            logger.info(f"Creating/finding parent folder: {parent_name}")
            parent_id = self.get_or_create_folder(parent_name, self.root_folder_id, session)

            type_label = 'Pickup' if upload_type == 'pickup' else 'Deliver'
            subfolder_name = f"{type_label}_{today}_{safe_driver}"
            logger.info(f"Creating/finding subfolder: {subfolder_name}")
            subfolder_id = self.get_or_create_folder(subfolder_name, parent_id, session)

            logger.info(f"Uploading '{file_name}' to folder '{subfolder_name}' (id={subfolder_id})")
            return self.upload_image(session, file_path, file_name, subfolder_id)
        except Exception as e:
            logger.error(f"validate_and_upload failed for '{file_name}': {e}", exc_info=True)
            raise
