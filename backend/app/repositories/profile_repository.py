# backend/app/repositories/profile_repository.py
"""Repository layer for Profile.
Handles direct SQLAlchemy operations; the service layer adds business rules.
"""

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.profile import Profile
from ..models.photo import Photo


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        result = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalars().first()

    async def create(
            self, 
            user_id: int,
            full_name: str
        ) -> Profile:
        profile = Profile(
            user_id=user_id,
            display_name=full_name,
        )
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

    async def set_photo(self, profile: Profile, photo: Photo) -> Profile:
        """Link a Photo to the Profile as the profile picture."""
        profile.profile_photo_id = photo.id
        return await self.update(profile)

    async def search(
        self,
        query: str | None = None,
        city: str | None = None,
        limit: int = 20,
    ) -> list[Profile]:
        """Search public profiles with a lightweight text query and optional city filter."""
        prof_search = select(Profile)
        filters = []

        if query and query.strip():
            term = f"%{query.strip()}%"
            filters.append(
                or_(
                    Profile.display_name.ilike(term),
                    Profile.city.ilike(term),
                    Profile.bio.ilike(term),
                )
            )

        if city and city.strip():
            city_term = f"%{city.strip()}%"
            filters.append(Profile.city.ilike(city_term))

        if filters:
            prof_search = prof_search.where(and_(*filters))

        prof_search = prof_search.order_by(Profile.created_at.desc()).limit(limit)
        result = await self.db.execute(prof_search)
        return result.scalars().all()
