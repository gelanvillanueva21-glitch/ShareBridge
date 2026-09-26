# backend/app/repositories/profile_repository.py
"""Repository layer for Profile.
Handles direct SQLAlchemy operations; the service layer adds business rules.
"""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.profile import Profile
from ..models.photo import Photo

class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_user_id(self, user_id: int) -> Profile | None:
        result = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalars().first()


    async def create(self, user_id: int) -> Profile:
        profile = Profile(user_id=user_id)
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile


    async def update(self, profile: Profile, **kwargs) -> Profile:
        for attr, value in kwargs.items():
            setattr(profile, attr, value)
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile


    async def set_photo(session: AsyncSession, profile: Profile, photo: Photo) -> Profile:
        profile.profile_photo_id = photo.id
        return await ProfileRepository.update(session, profile)
