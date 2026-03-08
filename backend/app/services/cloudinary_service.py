"""
app/services/cloudinary_service.py
"""
import hashlib
import time
from uuid import UUID

from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.transaction import CloudinarySignatureResponse


class CloudinaryService:

    def _is_configured(self) -> bool:
        return bool(
            settings.CLOUDINARY_CLOUD_NAME
            and settings.CLOUDINARY_API_KEY
            and settings.CLOUDINARY_API_SECRET
        )

    def get_upload_signature(self, user_id: UUID) -> CloudinarySignatureResponse:
        if not self._is_configured():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cloudinary is not configured. Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in your .env file.",
            )
        timestamp = int(time.time())
        year = time.strftime("%Y")
        folder = f"receipts/{user_id}/{year}"
        # Sign with allowed_formats so jpg/jpeg/png/pdf/webp/heic all pass
        params_to_sign = {
            "allowed_formats": "jpg,jpeg,png,webp,heic,pdf",
            "folder": folder,
            "timestamp": timestamp,
            "eager": "c_limit,w_1200,f_auto,q_auto",
        }

        string_to_sign = "&".join(
            f"{k}={v}"
            for k, v in sorted(params_to_sign.items())
        ) + settings.CLOUDINARY_API_SECRET

        signature = hashlib.sha1(string_to_sign.encode("utf-8")).hexdigest()
        
        return CloudinarySignatureResponse(
            signature=signature,
            timestamp=timestamp,
            folder=folder,
            api_key=settings.CLOUDINARY_API_KEY,
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        )
    