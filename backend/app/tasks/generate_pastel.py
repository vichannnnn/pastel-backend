import requests
from app.worker import celery_app
import random
from typing import Tuple, Optional

API_URL = "https://pastel.himaaa.xyz"
PASTEL_GENERATE_ENDPOINT = "/predictions"


@celery_app.task(name="generate_pastel_art")
def generate_pastel_art(prompt_input: Optional[str] = None) -> Tuple[str, str]:
    extra_random_prompt = (
        "red hair, blue hair, green hair, blonde hair, black hair, black eyes, red eyes, "
        "witch hat, school uniform, cat ears, gothic Lolita, maid outfit, kimono, "
        "sailor suit, bunny girl, angel wings, horns, princess dress, glasses, long hair, "
        "short hair, twin tails, odango (buns), beret, ribbon, choker, thigh-high stockings, "
        "knee-high boots, platform shoes, oversized sweater, denim shorts, leather jacket, "
        "skater skirt, crop top, hoodie, cat-eye sunglasses, flower crown, lace gloves, fingerless "
        "gloves, parasol, top hat, feather boa, frilly apron, suspender skirt, bandana, "
        "floral headband, heart-shaped sunglasses, backpack, sneakers, arm warmers, leg warmers, "
        "scarf, bowtie, halter top, high-waisted shorts, peplum dress, strappy sandals, "
        "feathered earrings, feathered necklace, ear cuffs, waist cincher, fishnet stockings, "
        "garter belt, sailor hat, military jacket, biker boots, striped tights, furry earmuffs, "
        "parka, fleece-lined leggings, fingerless mittens, feathered hair clip, cape, denim jacket, "
        "cutout boots, lacy thigh-highs, furry boots, floral dress, collared shirt, tweed blazer, "
        "corset top, jumpsuit, combat boots, fringed bag, wool coat, cable-knit sweater, "
        "cargo pants, lace-up boots, suede skirt, wide-brimmed hat, embroidered jacket, "
        "beaded bracelet, leather pants, sheer blouse, geometric earrings, diamond choker, "
        "velvet pumps, sequin dress, tassel earrings, ruffle skirt, cropped jacket, studded boots, "
        "peacock feather hair clip, crochet top, polka dot dress, silk scarf, fringe vest, "
        "pom-pom beanie".split(",")
    )

    prompt = "(mksks style), (masterpiece), (best quality), (ultra-detailed), (highres), illustration, portrait, 1girl"
    #  + ",".join(random.sample(extra_random_prompt, 5))

    if prompt_input:
        prompt += prompt_input
        
    negative_prompt = (
        "lowres, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, "
        "blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), "
        "(ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), "
        "((extra feet)), monster, logo, cropped, worst quality, low quality, normal quality, jpeg, "
        "humpbacked, long body, long neck, ((jpeg artifacts)) "
    )
    data = {
        "input": {
            "prompt": prompt,
            "neg_prompt": negative_prompt,
            "width": 448,
            "height": 640,
            "steps": 20,
            "guidance": 7,
            "seed": 0,
            "hires": True
        }
    }
    resp = requests.post(API_URL + PASTEL_GENERATE_ENDPOINT, json=data)
    return resp.json()["output"][0]
