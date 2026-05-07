import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.services.user_service import UserService

try:
    from jose import JWTError, jwt
except Exception:  # pragma: no cover - used only when optional deps are absent in local envs.
    JWTError = Exception
    jwt = None

try:
    from passlib.context import CryptContext
except Exception:  # pragma: no cover
    CryptContext = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None
bearer_scheme = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, user_id: str, email: str, name: str, is_dev: bool = False) -> None:
        self.id = user_id
        self.email = email
        self.name = name
        self.is_dev = is_dev


def hash_password(password: str) -> str:
    if pwd_context:
        return pwd_context.hash(password)
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    return f"pbkdf2_sha256${salt}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, password_hash: str) -> bool:
    if pwd_context:
        return pwd_context.verify(password, password_hash)
    try:
        scheme, salt, stored = password_hash.split("$", 2)
    except ValueError:
        return False
    if scheme != "pbkdf2_sha256":
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    expected = base64.urlsafe_b64encode(digest).decode()
    return hmac.compare_digest(expected, stored)


def create_access_token(user_id: str, email: str) -> str:
    settings = get_settings()
    if not settings.jwt_secret_key:
        raise RuntimeError("JWT_SECRET_KEY is required to issue access tokens.")
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {"sub": user_id, "email": email, "exp": expires_at}
    if jwt:
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return _encode_fallback_jwt(payload, settings.jwt_secret_key)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.jwt_secret_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is not configured.")
    try:
        if jwt:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        else:
            payload = _decode_fallback_jwt(token, settings.jwt_secret_key)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.") from exc
    if not payload.get("sub") or not payload.get("email"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> CurrentUser:
    settings = get_settings()
    if not settings.auth_enabled:
        if settings.app_env == "production":
            raise HTTPException(status_code=500, detail="AUTH_ENABLED=false is unsafe in production.")
        return CurrentUser("local-dev-user", "local-dev@nisf.dev", "Local Dev User", is_dev=True)

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")

    payload = decode_access_token(credentials.credentials)
    user = UserService().get_by_id(payload["sub"])
    if user is None or not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive or missing.")
    return CurrentUser(user["_id"], user["email"], user.get("name") or user["email"])


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _encode_fallback_jwt(payload: dict[str, Any], secret: str) -> str:
    serializable = payload.copy()
    if isinstance(serializable.get("exp"), datetime):
        serializable["exp"] = int(serializable["exp"].timestamp())
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = ".".join(
        [
            _b64encode(json.dumps(header, separators=(",", ":")).encode()),
            _b64encode(json.dumps(serializable, separators=(",", ":")).encode()),
        ]
    )
    signature = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f"{signing_input}.{_b64encode(signature)}"


def _decode_fallback_jwt(token: str, secret: str) -> dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".", 2)
    except ValueError as exc:
        raise JWTError("Malformed token") from exc
    signing_input = f"{header_b64}.{payload_b64}"
    expected = _b64encode(hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(expected, signature_b64):
        raise JWTError("Invalid signature")
    payload = json.loads(_b64decode(payload_b64))
    if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
        raise JWTError("Expired token")
    return payload
