from app.schemas.template_schema import TemplateOut


class TemplateService:
    def list_templates(self) -> list[TemplateOut]:
        return [
            TemplateOut(
                id="linkedin-ad",
                name="LinkedIn Ad",
                content_type="ad",
                description="Concise B2B campaign copy for LinkedIn.",
                prompt_pattern="Audience + pain point + differentiated benefit + CTA",
            ),
            TemplateOut(
                id="email-subject",
                name="Email Subject",
                content_type="email",
                description="Short subject-line copy optimized for opens.",
                prompt_pattern="Specific outcome + curiosity + low friction",
            ),
        ]
