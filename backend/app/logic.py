from app.schemas.core import PastelPrompt


BASE_PROMPT = "(mksks style), (masterpiece), (best quality), (ultra-detailed), (highres), illustration, portrait, 1girl"

NEGATIVE_PROMPT = (
    "lowres, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, blurry, "
    "((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), (ugly), "
    "((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), ((extra feet)), "
    "monster, logo, cropped, worst quality, low quality, normal quality, jpeg, humpbacked, long body, "
    "long neck, ((jpeg artifacts)) "
)


def prompt_input(prompt: PastelPrompt) -> dict:
    data = {
        "input": {
            "prompt": prompt.prompt_input,
            "neg_prompt": prompt.negative_prompt_input,
            "width": 448,
            "height": 640,
            "steps": 20,
            "guidance": 7,
            "seed": 0,
            "hires": True,
        }
    }
    return data
