from typing import Optional
from pydantic import BaseModel


class PastelPromptInput(BaseModel):
    prompt_input: Optional[str] = None
