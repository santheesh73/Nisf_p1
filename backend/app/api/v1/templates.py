from fastapi import APIRouter

from app.schemas.template_schema import TemplateOut
from app.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=list[TemplateOut])
def list_templates() -> list[TemplateOut]:
    return TemplateService().list_templates()
