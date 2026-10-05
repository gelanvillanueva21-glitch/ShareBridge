# backend/app/repositories/photo_repository.py
"""Repository for handling photo uploads.

The repository persists a :class:`Photo` record with the generated filename
(and the appropriate purpose) and returns the ORM instance.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.utils.image_helper import save_image
from app.models.photo import Photo, PhotoPurpose


class PhotoRepository:
    """
        This PhotoRepository handles all the database
        operation of the sending pictures by the users.
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
