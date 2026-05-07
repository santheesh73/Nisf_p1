import uuid
from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from app.core.exceptions import NISFError
from app.db.mongo import USERS, get_sync_collection


class DuplicateEmailError(NISFError):
    status_code = 409
    code = "duplicate_email"


class UserService:
    """MongoDB-backed user CRUD with public response shaping."""

    def _collection(self):
        return get_sync_collection(USERS)

    def create_user(self, *, email: str, password_hash: str, name: str) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        doc = {
            "_id": str(uuid.uuid4()),
            "email": email.strip().lower(),
            "password_hash": password_hash,
            "name": name.strip(),
            "created_at": now,
            "updated_at": now,
            "is_active": True,
        }
        try:
            self._collection().insert_one(doc)
        except DuplicateKeyError as exc:
            raise DuplicateEmailError("A user with this email already exists.") from exc
        return doc

    def get_by_email(self, email: str) -> dict | None:
        return self._collection().find_one({"email": email.strip().lower()})

    def get_by_id(self, user_id: str) -> dict | None:
        return self._collection().find_one({"_id": user_id})

    def public_user(self, user: dict) -> dict:
        return {
            "id": user["_id"],
            "email": user["email"],
            "name": user.get("name") or user["email"],
        }
