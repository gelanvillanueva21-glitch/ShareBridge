# backend/app/services/profile_service.py
"""Service layer for Profile.
Implements business rules and orchestrates repository calls.
The class is instantiated via a dependency defined in `app.utils.dependencies`.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.profile_repository import ProfileRepository
from app.repositories.photo_repository import PhotoRepository
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate
from fastapi import UploadFile
from app.utils.image_helper import save_image


class ProfileService:
    """Instantiated per request with a DB session and a ProfileRepository.
    All methods receive the authenticated user via the `CurrentUser` dependency.
    """

    def __init__(self, db: AsyncSession, repo: ProfileRepository):
        self.db = db
        self.repo = repo

    async def get_my_profile(self, current_user: User):
        """Return the profile for the current user, creating it lazily if missing."""
        profile = await self.repo.get_by_user_id(current_user.id)
        if not profile:
            profile = await self.repo.create(
                current_user.id,
                current_user.full_name
            )
        return profile

    async def update_my_profile(
        self,
        payload: ProfileUpdate,
        current_user: User,
    ):
        """Partial update of the current user's profile."""
        profile = await self.repo.get_by_user_id(current_user.id)
        if not profile:
            profile = await self.repo.create(current_user.id)
        update_data = payload.model_dump(exclude_unset=True)
        return await self.repo.update(profile, **update_data)

    async def upload_profile_photo(
        self,
        file: UploadFile,
        current_user: User,
    ):
        """Handle multipart upload, store the photo, and link it to the profile."""
        photo = await PhotoRepository(self.db).create_profile_photo(
            current_user.id,
            await save_image(file),
        )
        profile = await self.repo.get_by_user_id(current_user.id)
        if not profile:
            profile = await self.repo.create(current_user.id)
        await self.repo.set_photo(profile, photo)
        profile.profile_photo_url = f"/avatars/{photo.file_path}"
        return profile

    async def search_profiles(
        self,
        query: str | None = None,
        city: str | None = None,
    ) -> list[Profile]:
        """Search by a lightweight text term across name, city, and bio."""
        if query is not None:
            query = query.strip()
        if city is not None:
            city = city.strip()

        if not query and not city:
            return []

        return await self.repo.search(
            query=query,
            city=city,
        )
