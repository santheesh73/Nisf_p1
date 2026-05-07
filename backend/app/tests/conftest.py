import pytest

from app.core.config import get_settings


@pytest.fixture(autouse=True)
def default_local_auth_disabled():
    settings = get_settings()
    original_auth_enabled = settings.auth_enabled
    original_app_env = settings.app_env
    settings.auth_enabled = False
    settings.app_env = "local"
    yield
    settings.auth_enabled = original_auth_enabled
    settings.app_env = original_app_env
