import requests
from app.worker import celery_app
from app.schemas.core import PastelPrompt
from app.models.core import PastelArt
from fastapi.encoders import jsonable_encoder
import base64
import random
from faker import Faker
from app.exceptions import AppError
import psycopg
import os
from psycopg import sql
from typing import Dict


DB_URL = os.environ["TASK_RUNNER_DATABASE_URL"]
API_URL = os.environ["MODELLING_API_URL"]
PASTEL_GENERATE_ENDPOINT = "/predictions"


@celery_app.task(name="generate_pastel_art")
def generate_pastel_art(prompt: Dict[str, str]) -> str:

    data = {
        "input": {
            **prompt,
            "width": 448,
            "height": 640,
            "steps": 20,
            "guidance": 7,
            "seed": 0,
            "hires": True,
        }
    }

    resp = requests.post(API_URL + PASTEL_GENERATE_ENDPOINT, json=data)
    try:
        img_string = resp.json()["output"][0]

    except IndexError as e:
        raise AppError.NSFW_ERROR from e

    img_string = img_string.split(",")[1]
    img_data = base64.b64decode(img_string)

    fake = Faker()
    image_name = (
        f"{fake.word()}_{fake.word()}_{fake.word()}_{random.randint(1000, 99999)}.png"
    )
    file_name = f"/app/images/{image_name}"

    with open(file_name, "wb") as f:
        f.write(img_data)

    data["input"].pop("hires")
    pastel_obj = PastelArt(**data["input"])
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            table = "pastel_art"
            columns = (
                "prompt",
                "neg_prompt",
                "width",
                "height",
                "steps",
                "guidance",
                "seed",
                "image",
            )
            values = (
                pastel_obj.prompt,
                pastel_obj.neg_prompt,
                pastel_obj.width,
                pastel_obj.height,
                pastel_obj.steps,
                pastel_obj.guidance,
                pastel_obj.seed,
                image_name,
            )
            insert_stmt = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(sql.SQL("%s") for _ in values),
            )
            cur.execute(insert_stmt, values)
        conn.commit()
    return resp.json()["output"][0]


# @celery_app.task(name="automated_generate_pastel_art_task")
# def automated_generate_pastel_art_task() -> str:
#     types = {
#         'type': random.choice([PromptType.RANDOM, PromptType.DEFAULT])
#     }
#     prompt = PastelPrompt(**types)
#     data = prompt_input(prompt)
#     resp = requests.post(API_URL + PASTEL_GENERATE_ENDPOINT, json=data)
#     try:
#         img_string = resp.json()["output"][0]
#
#     except IndexError as e:
#         raise AppError.NSFW_ERROR from e
#
#     img_string = img_string.split(",")[1]
#     img_data = base64.b64decode(img_string)
#
#     fake = Faker()
#     image_name = f"{fake.word()}_{fake.word()}_{random.randint(1000, 9999)}.png"
#     file_name = f"/app/images/{image_name}"
#
#     with open(file_name, "wb") as f:
#         f.write(img_data)
#
#     data['input'].pop("hires")
#     pastel_obj = PastelArt(**data['input'])
#     with psycopg.connect(DB_URL) as conn:
#         with conn.cursor() as cur:
#             table = "pastel_art"
#             columns = (
#                 "prompt",
#                 "neg_prompt",
#                 "width",
#                 "height",
#                 "steps",
#                 "guidance",
#                 "seed",
#                 "image",
#             )
#             values = (
#                 pastel_obj.prompt,
#                 pastel_obj.neg_prompt,
#                 pastel_obj.width,
#                 pastel_obj.height,
#                 pastel_obj.steps,
#                 pastel_obj.guidance,
#                 pastel_obj.seed,
#                 image_name,
#             )
#             insert_stmt = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
#                 sql.Identifier(table),
#                 sql.SQL(", ").join(map(sql.Identifier, columns)),
#                 sql.SQL(", ").join(sql.SQL("%s") for _ in values),
#             )
#             cur.execute(insert_stmt, values)
#         conn.commit()
#     return resp.json()["output"][0]
