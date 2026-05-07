from pydantic import BaseModel


class TemplateOut(BaseModel):
    id: str
    name: str
    content_type: str
    description: str
    prompt_pattern: str
