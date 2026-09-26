# backend/app/repositories/profile_repository.py
"""Repository layer for Profile.
Handles direct SQLAlchemy operations; the service layer adds business rules.
"""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from ..models.profile import Profile
from ..models.photo import Photo

class ProfileRepository:
    @staticmethod
    async def get_by_user_id(session: AsyncSession, user_id: int) -> Profile | None:
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalars().first()

    @staticmethod
    async def create(session: AsyncSession, user_id: int) -> Profile:
        profile = Profile(user_id=user_id)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile

    @staticmethod
    async def update(session: AsyncSession, profile: Profile, **kwargs) -> Profile:
        for attr, value in kwargs.items():
            setattr(profile, attr, value)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile

    @staticmethod
    async def set_photo(session: AsyncSession, profile: Profile, photo: Photo) -> Profile:
        profile.profile_photo_id = photo.id
        return await ProfileRepository.update(session, profile)
