# backend/app/repositories/photo_repository.py
"""Repository for handling photo uploads.

The repository persists a :class:`Photo` record with the generated filename
(and the appropriate purpose) and returns the ORM instance.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.utils.picture_utils import save_picture
from app.models.photo import Photo, PhotoPurpose


class PhotoRepository:
    """Repository handling creation of :class:`Photo` entries.

    The repository is lightweight – it only needs the DB session to create the
    ``Photo`` record. The actual file is saved by :func:`save_picture`, which
    returns the generated filename (without any path prefix).
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile_photo(self, uploader_id: int, file_url: str) -> Photo:
        """Save the uploaded file and create a ``Photo`` entry for a profile picture.

        Returns the newly persisted ``Photo`` ORM instance.
        """
        # Store the file under the ``profile_pictures`` sub‑folder.

        photo = Photo(
            uploader_id=uploader_id,
            file_path=file_url,
            purpose=PhotoPurpose.PROFILE,
            reference_id=uploader_id,
        )
        self.db.add(photo)
        await self.db.commit()
        await self.db.refresh(photo)
        return photo
