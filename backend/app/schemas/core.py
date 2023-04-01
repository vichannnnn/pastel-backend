from enum import Enum
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    page: int
    size: int
    total: int


class PromptType(str, Enum):
    RANDOM = "RANDOM"
    CUSTOM = "CUSTOM"


class PastelPrompt(BaseModel):
    prompt: str
    neg_prompt: str


class PastelImage(BaseModel):
    row_id: int
    prompt: str
    neg_prompt: str
    width: int
    height: int
    steps: int
    guidance: int
    image: str
    seed: int
