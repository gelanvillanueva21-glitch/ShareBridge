from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.exceptions import AlreadyExistsError, InvalidCredentialsError


class UserService:
    """
    Handles ALL business logic for users.

    This class has ONE job: enforce business rules.
    It does NOT know about HTTP. It raises custom AppErrors,
    and the router layer catches them and converts them to HTTP responses.

    Constructor receives both the database session and the repository.
    The repository is the only thing that touches the database directly.
    """

    def __init__(self, db: AsyncSession, repo: UserRepository):
        self.db = db
        self.repo = repo

    async def register(self, user_in: UserCreate) -> User:
        """
        Business rule: an email can only be registered once.
        1. Check if email already exists via repository.
        2. Hash the password.
        3. Delegate the actual insert to the repository.
        """
        existing = await self.repo.get_by_email(user_in.email)
        if existing:
            raise AlreadyExistsError("An account with this email already exists.")

        hashed = hash_password(user_in.password)

        return await self.repo.create(
            email=user_in.email,
            hashed_password=hashed,
            display_name=user_in.display_name,
            role=user_in.role,
        )

    async def authenticate(self, email: str, password: str) -> User:
        """
        Business rule: both the user must exist and the password must match.
        Raises InvalidCredentialsError for either failure — deliberately vague
        so attackers cannot tell if the email exists or not.
        """
        user = await self.repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password.")

        return user

    async def get_by_id(self, user_id: int) -> User:
        """
        Returns a user by ID.
        Raises NotFoundError if the user does not exist.
        """
        from app.exceptions import NotFoundError
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} was not found.")
        return user
