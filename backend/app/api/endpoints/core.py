from fastapi import APIRouter, Depends, Query
from app.tasks.generate_pastel import generate_pastel_art
from app.schemas.core import PastelPrompt, PastelImage
from app.models.core import PastelArt
from app.db.database import AsyncSession
from app.api.deps import get_session
from fastapi_pagination import Page


router = APIRouter()


@router.post("/generate_pastel_art")
async def trigger_generate_pastel_art(prompt: PastelPrompt):
    task = generate_pastel_art.delay(dict(prompt))
    return {"task_id": task.id}


@router.get("/get_all", response_model=Page[PastelImage])
async def get_all_pastel_images(
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, title="Page number", gt=0),
    size: int = Query(50, title="Page size", gt=0, le=1000),
):
    data, total = await PastelArt.get_all(page=page, size=size, session=session)
    return Page[PastelImage](
        items=data,
        page=page,
        size=size,
        total=total,
    )


@router.get("/generate_pastel_art/{task_id}")
def crawling_status(task_id: str):
    task = generate_pastel_art.AsyncResult(task_id)

    if task.state == "PENDING":  # pylint: disable=no-else-return
        return {"status": "pending"}
    elif task.state == "SUCCESS":
        return {"status": "success", "result": task.result}
    else:
        return {"status": "failure", "error": str(task.result)}
