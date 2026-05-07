from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import CurrentUser, create_access_token, get_current_user, hash_password, verify_password
from app.core.config import get_settings
from app.schemas.auth_schema import AuthConfigResponse, AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/config", response_model=AuthConfigResponse)
def get_auth_config() -> AuthConfigResponse:
    settings = get_settings()
    return AuthConfigResponse(
        auth_enabled=settings.auth_enabled,
        local_dev_mode=not settings.auth_enabled and settings.app_env == "local",
    )


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest) -> AuthResponse:
    service = UserService()
    if service.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists.")
    user = service.create_user(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
    )
    token = _issue_token(user["_id"], user["email"])
    return AuthResponse(user=AuthUser(**service.public_user(user)), access_token=token)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    service = UserService()
    user = service.get_by_email(payload.email)
    if user is None or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    if not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive.")
    token = _issue_token(user["_id"], user["email"])
    return AuthResponse(user=AuthUser(**service.public_user(user)), access_token=token)


@router.get("/me", response_model=AuthUser)
def me(current_user: CurrentUser = Depends(get_current_user)) -> AuthUser:
    return AuthUser(id=current_user.id, email=current_user.email, name=current_user.name)


def _issue_token(user_id: str, email: str) -> str:
    try:
        return create_access_token(user_id, email)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is enabled but JWT_SECRET_KEY is not configured.",
        ) from exc
