from fastapi import APIRouter
from app.tasks.generate_pastel import generate_pastel_art

router = APIRouter()


@router.get("/hello")
async def sanity_check():
    return {"Hello": "World!"}


@router.post("/generate_pastel_art")
async def trigger_generate_pastel_art():
    task = generate_pastel_art.delay()
    return {"task_id": task.id}


@router.get("/generate_pastel_art/{task_id}")
def crawling_status(task_id: str):
    task = generate_pastel_art.AsyncResult(task_id)

    if task.state == "PENDING":  # pylint: disable=no-else-return
        return {"status": "pending"}
    elif task.state == "SUCCESS":
        return {"status": "success", "result": task.result}
    else:
        return {"status": "failure", "error": str(task.result)}
