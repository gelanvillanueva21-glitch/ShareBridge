from fastapi import APIRouter, HTTPException, status, Response, Cookie
from typing import Optional
from jose import JWTError

from app.utils.dependencies import UserServiceDep, CurrentUser, UserRepo
from app.utils.security import create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate, UserRead, TokenResponse, LoginRequest
from app.exceptions import AlreadyExistsError, InvalidCredentialsError, NotFoundError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, 
    service: UserServiceDep
):
    """
    POST /api/auth/register
    Creates a new user account. Password is hashed by the service layer.
    Returns the new user profile (without the password).
    """
    try:
        user = await service.register(user_in)
        return user
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest, 
    response: Response, 
    service: UserServiceDep
):
    """
    POST /api/auth/login
    Verifies credentials and returns:
    - Access Token in the JSON body (stored in React state, gone on refresh).
    - Refresh Token as an HttpOnly cookie (browser stores it, JS cannot read it).
    """
    try:
        user = await service.authenticate(credentials.email, credentials.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,              # JS cannot read this — blocks XSS attacks
        secure=True,                # Only sent over HTTPS in production
        samesite="lax",             # Blocks CSRF from other origins
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )

    return TokenResponse(access_token=access_token, user=UserRead.model_validate(user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    repo: UserRepo,
    refresh_token: Optional[str] = Cookie(default=None),
):
    """
    POST /api/auth/refresh
    The browser sends the HttpOnly cookie automatically.
    If valid, returns a new Access Token so the user stays logged in silently.
    """
    session_expired = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session expired. Please log in again.",
    )

    if not refresh_token:
        raise session_expired

    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise session_expired
    except JWTError:
        raise session_expired

    user = await repo.get_by_id(int(user_id))
    if not user:
        raise session_expired

    new_access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(
        access_token=new_access_token,
        user=UserRead.model_validate(user),
    )


@router.post("/logout")
async def logout(response: Response):
    """
    POST /api/auth/logout
    Clears the HttpOnly refresh token cookie.
    The Access Token in React state disappears automatically on page close.
    """
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully."}


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    """
    GET /api/auth/me
    Protected route. Returns the authenticated user's profile.
    'CurrentUser' is an Annotated alias — no boilerplate Depends() needed here.
    """
    return current_user
