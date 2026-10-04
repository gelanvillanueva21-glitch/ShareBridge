# backend/app/repositories/photo_repository.py
"""Repository for handling photo uploads.

The repository persists a :class:`Photo` record with the generated filename
(and the appropriate purpose) and returns the ORM instance.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.utils.picture_utils import save_picture, remove_picture
from app.models.photo import Photo, PhotoPurpose
from app.exceptions import NotFoundError


class PhotoRepository:
    """Repository handling creation of :class:`Photo` entries.

    The repository is lightweight – it only needs the DB session to create the
    ``Photo`` record. The actual file is saved by :func:`save_picture`, which
    returns the generated filename (without any path prefix).
    """

    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_photo(
        self, 
        uploader_id: int, 
        file_url: str, 
        purpose: PhotoPurpose, 
    ) -> Photo:
        """
        This function save a photo depending of the purpose
        the database already handle the reference of what the photo is for, 
        so we just need to pass the reference_id
        """
        photo = Photo(
            uploader_id=uploader_id,
            file_path=file_url,
            purpose=purpose
        )
        self.db.add(photo)
        await self.db.commit()
        await self.db.refresh(photo)
        return photo


    async def get_by_id(self, photo_id: int) -> Photo  | None:
        result = await self.db.execute(
            select(
                Photo
            ).where(
                Photo.id == photo_id
            )
        )
        return result.scalar_one_or_none()
