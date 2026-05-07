from fastapi import APIRouter, Depends, Request

from app.core.rate_limit import protect_endpoint
from app.core.auth import CurrentUser, get_current_user
from app.schemas.generate_schema import GenerateTextRequest, GenerateTextResponse, GenerateVariant
from app.services.generation.generation_service import GenerationService

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/text", response_model=GenerateTextResponse)
def generate_text(
    request: GenerateTextRequest,
    _: Request,
    __: None = Depends(protect_endpoint("generate")),
    _current_user: CurrentUser = Depends(get_current_user),
) -> GenerateTextResponse:
    service = GenerationService()
    generated = service.generate_variants(
        text=request.text,
        brief=request.brief,
        content_type=request.content_type,
        tone=request.tone,
        platform=request.platform,
        count=request.variant_count,
        brand_terms=request.brand_terms,
    )
    variants = [
        GenerateVariant(
            id=f"v{index}",
            text=text,
            metadata={
                "content_type": request.content_type,
                "tone": request.tone,
                "platform": request.platform,
            },
        )
        for index, text in enumerate(generated, start=1)
    ]
    return GenerateTextResponse(
        provider=service.provider_name,
        model=service.model_name,
        variant_count=len(variants),
        variants=variants,
    )
