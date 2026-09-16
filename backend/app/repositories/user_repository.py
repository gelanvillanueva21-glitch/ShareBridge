from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    """
    Handles ALL database operations for the User table.
    This class has ONE job: talk to the database.
    No business logic. No error raising. Just pure data access.

    The constructor receives the database session, which is injected
    by FastAPI's dependency system — this class never creates its own session.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """Returns a User by their primary key ID, or None if not found."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Returns a User by their email address, or None if not found."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        hashed_password: str,
        display_name: str | None,
        role,
    ) -> User:
        """
        Inserts a new User row into the database.
        Returns the newly created User object with its generated ID.
        """
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            display_name=display_name,
            role=role,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_verified(self, user: User, is_verified: bool) -> User:
        """Sets the is_verified flag on a user. Used by admins."""
        user.is_verified = is_verified
        await self.db.commit()
        await self.db.refresh(user)
        return user

