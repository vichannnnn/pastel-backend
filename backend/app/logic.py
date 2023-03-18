import random
from app.schemas.core import PastelPrompt, PromptType
from typing import Optional


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

base_prompt = "(mksks style), (masterpiece), (best quality), (ultra-detailed), (highres), illustration, portrait, 1girl"

negative_prompt = (
    "lowres, ((bad anatomy)), ((bad hands)), ((((((((((bad fingers)))))))))), text, missing finger, extra digits, "
    "fewer digits, "
    "blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), ((poorly drawn eye)),"
    "(ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), "
    "((extra feet)), monster, logo, cropped, worst quality, low quality, normal quality, jpeg, "
    "humpbacked, long body, long neck, ((jpeg artifacts)) "
)


def prompt_input(prompt: Optional[PastelPrompt]) -> dict:

    if prompt.type == PromptType.Custom:
        res_prompt = base_prompt + prompt.input

    elif prompt.type == PromptType.Random:
        res_prompt = base_prompt + ",".join(random.sample(extra_random_prompt, 5))

    else:
        res_prompt = base_prompt

    data = {
        "input": {
            "prompt": res_prompt,
            "neg_prompt": negative_prompt,
            "width": 448,
            "height": 640,
            "steps": 20,
            "guidance": 9,
            "seed": 0,
            "hires": True,
        }
    }
    return data
