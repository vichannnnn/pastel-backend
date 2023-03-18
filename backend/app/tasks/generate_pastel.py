import requests
from app.worker import celery_app
from app.schemas.core import PastelPrompt, PromptType
from app.logic import prompt_input
from typing import Tuple, Optional

API_URL = "https://pastel.himaaa.xyz"
PASTEL_GENERATE_ENDPOINT = "/predictions"


@celery_app.task(name="generate_pastel_art")
def generate_pastel_art(prompt: PastelPrompt = None) -> Tuple[str, str]:

    data = prompt_input(prompt)
    resp = requests.post(API_URL + PASTEL_GENERATE_ENDPOINT, json=data)
    return resp.json()["output"][0]
