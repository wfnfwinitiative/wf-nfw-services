# google_drive_router.py
import logging
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.google_drive_repository import GoogleDriveRepository
from app.services.opportunity_service import OpportunityService

logger = logging.getLogger(__name__)

router = APIRouter()
drive_repo = GoogleDriveRepository()


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    upload_type: str = Form("pickup"),
    driver_name: str = Form("Driver"),
    opportunity_id: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    """Upload image to Google Drive using stored refresh token from env.

    If an opportunity ID is provided, we attempt to store/reuse the Drive folder
    ID in the opportunity record (pickup_folder_id or delivery_folder_id).
    """

    if upload_type not in {"pickup", "delivery"}:
        raise HTTPException(
            status_code=400, detail="upload_type must be either 'pickup' or 'delivery'"
        )

    folder_field = None
    existing_folder_id = None
    opportunity_obj = None

    if opportunity_id:
        try:
            opportunity_obj = await OpportunityService(db).get_opportunity(
                int(opportunity_id)
            )
            if upload_type == "pickup":
                folder_field = "pickup_folder_id"
            elif upload_type == "delivery":
                folder_field = "delivery_folder_id"

            if folder_field:
                existing_folder_id = getattr(opportunity_obj, folder_field)
        except Exception:
            # If the provided opportunity_id is invalid or missing, continue without persistence
            opportunity_obj = None
            existing_folder_id = None

    temp_path = None
    try:
        suffix = os.path.splitext(file.filename)[1] if file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            temp_path = tmp.name

        logger.info(
            f"Uploading '{file.filename}' | type={upload_type} | driver={driver_name} | opp={opportunity_id}"
        )

        result = drive_repo.validate_and_upload(
            temp_path,
            file.filename,
            upload_type,
            driver_name,
            opportunity_id,
            existing_folder_id=existing_folder_id,
        )

        # Persist folder id for future uploads if we just created it
        if opportunity_obj and folder_field and not existing_folder_id:
            folder_id = result.get("folder_id")
            if folder_id:
                await OpportunityService(db).update_opportunity(
                    opportunity_obj.opportunity_id,
                    **{folder_field: folder_id},
                )

        return {
            "success": True,
            "file": result.get("file"),
            "folder_id": result.get("folder_id"),
        }
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass


@router.get("/oauth2callback")
def oauth2callback(request: Request):
    """
    Handle Google OAuth redirect, exchange code for tokens.
    Save refresh token to file for server-side use.
    """
    logger.info("OAuth2 callback received")
    logger.info(f"Full callback URL: {request.url}")
    logger.info(f"All query params: {dict(request.query_params)}")

    code = request.query_params.get("code")
    if not code:
        logger.error("Missing authorization code in callback")
        return {"error": "Missing authorization code"}

    logger.info(f"Authorization code received (first 20 chars): {code[:20]}...")

    try:
        logger.info("Attempting to exchange code for tokens with Google...")
        access_token, refresh_token = drive_repo.exchange_code_for_tokens(code)
        logger.info("Token exchange successful")
        logger.info(f"Access token received (first 20 chars): {access_token[:20]}...")
        logger.info(f"Refresh token received: {'YES' if refresh_token else 'NO'}")

        # Save refresh token to file
        token_path = "app/core/google_refresh_token.txt"
        with open(token_path, "w") as token_file:
            token_file.write(refresh_token)
        logger.info(f"Refresh token saved to {token_path}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Refresh token saved to server.",
        }
    except Exception as e:
        logger.error(f"OAuth2 callback error: {str(e)}", exc_info=True)
        return {"error": str(e)}
