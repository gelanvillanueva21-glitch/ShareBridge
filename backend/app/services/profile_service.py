# backend/app/services/profile_service.py
"""Service layer for Profile.
Implements business rules and orchestrates repository calls.
The class is instantiated via a dependency defined in `app.utils.dependencies`.
"""

from app.utils.db_session import DbSession
from app.utils.repositories import ProfileRepo
from app.utils.dependencies import CurrentUser
from ..repositories.photo_repository import PhotoRepository  # assumed to exist
from ..models.user import User
from ..schemas.profile import ProfileUpdate

class ProfileService:
    """Instantiated per request with a DB session and a ProfileRepository.
    All methods receive the authenticated user via the `CurrentUser` dependency.
    """


    def __init__(self, db: DbSession, repo: ProfileRepo):
        self.db = db
        self.repo = repo


    async def get_my_profile(self, current_user: CurrentUser):
        """Return the profile for the current user, creating it lazily if missing."""
        profile = await self.repo.get_by_user_id(self.db, current_user.id)
        if not profile:
            profile = await self.repo.create(self.db, current_user.id)
        return profile


    async def update_my_profile(self, payload: ProfileUpdate, current_user: CurrentUser):
        """Partial update of the current user's profile."""
        profile = await self.repo.get_by_user_id(self.db, current_user.id)
        if not profile:
            profile = await self.repo.create(self.db, current_user.id)
        update_data = payload.dict(exclude_unset=True)
        updated = await self.repo.update(self.db, profile, **update_data)
        return updated


    async def upload_profile_photo(self, file, current_user: CurrentUser):
        """Handle multipart upload, store the photo, and link it to the profile."""
        photo = await PhotoRepository.create_profile_photo(self.db, current_user.id, file)
        profile = await self.repo.get_by_user_id(self.db, current_user.id)
        if not profile:
            profile = await self.repo.create(self.db, current_user.id)
        profile = await self.repo.set_photo(self.db, profile, photo)
        return profile
