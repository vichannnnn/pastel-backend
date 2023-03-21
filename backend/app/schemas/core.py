from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PromptType(str, Enum):
    RANDOM = "RANDOM"
    DEFAULT = "DEFAULT"
    CUSTOM = "CUSTOM"


class PastelPrompt(BaseModel):
    input: Optional[str] = None
    type: PromptType = PromptType.DEFAULT


class PastelImage(BaseModel):
    row_id: int
    prompt: str
    negative_prompt: str
    width: int
    height: int
    steps: int
    guidance: int
    image: str
    seed: int
