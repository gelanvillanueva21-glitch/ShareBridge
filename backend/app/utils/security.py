import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import settings

# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    """
    Takes a plain text password and returns a bcrypt hash.
    bcrypt automatically handles salting — every hash is unique even for
    the same password, which prevents rainbow table attacks.
    """
    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password against the stored bcrypt hash.
    Returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ---------------------------------------------------------------------------
# JWT Token Creation
# ---------------------------------------------------------------------------

def create_access_token(data: dict) -> str:
    """
    Creates a short-lived JWT Access Token (15 minutes).
    This is sent in the Authorization header: "Bearer <token>".
    Stored in React state (memory) — gone on page refresh.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    """
    Creates a long-lived JWT Refresh Token (7 days).
    This is stored in an HttpOnly cookie — JavaScript cannot read it.
    When the Access Token expires, the browser automatically sends this
    cookie to /auth/refresh to get a new Access Token silently.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload.update({"exp": expire, "type": "refresh"})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# ---------------------------------------------------------------------------
# JWT Token Verification
# ---------------------------------------------------------------------------

def decode_token(token: str) -> dict:
    """
    Decodes and validates a JWT token.
    Raises JWTError if the token is expired, tampered with, or invalid.
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
