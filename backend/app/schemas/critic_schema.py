from pydantic import BaseModel


class CriticDirectiveSchema(BaseModel):
    target_dimension: str
    issue: str
    rewrite_instruction: str
    priority: int
    risk_level: str
