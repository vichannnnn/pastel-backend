from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PromptType(str, Enum):
    Random = "RANDOM"
    Default = "DEFAULT"
    Custom = "CUSTOM"


class PastelPrompt(BaseModel):
    input: Optional[str] = None
    type: PromptType
