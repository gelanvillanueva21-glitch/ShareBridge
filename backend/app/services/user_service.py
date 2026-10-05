
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.repositories.profile_repository import ProfileRepository



from app.utils.security import create_access_token, create_refresh_token
from app.schemas.user import TokenResponse, UserRead
from app.exceptions import AlreadyExistsError, InvalidCredentialsError, PermissionDeniedError


class UserService:
    """
    Handles ALL business logic for users.

    This class has ONE job: enforce business rules.
    It does NOT know about HTTP. It raises custom AppErrors,
    and the router layer catches them and converts them to HTTP responses.

    Constructor receives both the database session and the repository.
    The repository is the only thing that touches the database directly.
    """

    def __init__(
        self, 
        db: AsyncSession, 
        repo: UserRepository, 
        prof_repo: ProfileRepository
    ):
        self.db = db
        self.repo = repo
        self.prof_repo = prof_repo  

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

        if user_in.role == UserRole.ADMIN:
            raise PermissionDeniedError("Cannot create an account role admin!")

        hashed = hash_password(user_in.password)

        result = await self.repo.create(
            email=user_in.email,
            hashed_password=hashed,
            full_name=user_in.full_name,
            role=user_in.role,
        )

        # Instantly create profile after successfully create account
        await self.prof_repo.create(
            user_id=result.id, 
            full_name=result.full_name
        )
        return result


    async def authenticate(
        self, 
        email: str, 
        password: str, 
        response: Response
    ) -> TokenResponse:
        """
        Business rule: both the user must exist and the password must match.
        Raises InvalidCredentialsError for either failure — deliberately vague
        so attackers cannot tell if the email exists or not.
        """
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password.")


        # Create JWTs
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})


        # Set HttpOnly refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )
        return TokenResponse(access_token=access_token, )


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
