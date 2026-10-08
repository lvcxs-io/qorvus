from datetime import datetime, timedelta, timezone

import jwt
from pwdlib.exceptions import UnknownHashError
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()
_jwt_algorithm = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(password, hashed_password)
    except UnknownHashError:
        return False


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expires_at,
            "iss": "qorvus-api",
            "aud": "qorvus-web",
        },
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=_jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    claims = jwt.decode(
        token,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=[_jwt_algorithm],
        issuer="qorvus-api",
        audience="qorvus-web",
        options={"require": ["exp", "sub"]},
    )
    subject = claims["sub"]
    if not isinstance(subject, str) or not subject.isdecimal():
        raise jwt.InvalidTokenError("Token subject must be a user ID.")
    return int(subject)
