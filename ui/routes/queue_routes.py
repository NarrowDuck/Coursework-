from fastapi import APIRouter, Depends, Request, Form, responses, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dal.database import get_db
from dal.repositories import UserRepository, QueueRepository, QueueEntryRepository
from bll.services import QueueService
from bll.exceptions import QueueBaseException

router = APIRouter(tags=["Queues"])
templates = Jinja2Templates(directory="ui/templates")

def get_service(db: Session = Depends(get_db)):
    return QueueService(UserRepository(db), QueueRepository(db), QueueEntryRepository(db))

@router.get("/")
def index(request: Request, service: QueueService = Depends(get_service)):
    queues = service.q_repo.get_all()
    user_id = request.cookies.get("user_id")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"queues": queues, "user_id": int(user_id) if user_id else None}
    )

@router.get("/queues/create")
def create_queue_page(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(request=request, name="create_queue.html")

@router.post("/queues/create")
def create_queue(
        request: Request,
        name: str = Form(...),
        service: QueueService = Depends(get_service)
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    service.create_queue(name=name, owner_id=int(user_id))
    return responses.RedirectResponse(url="/", status_code=303)

@router.get("/queues/{queue_id}")
def view_queue(queue_id: int, request: Request, service: QueueService = Depends(get_service)):
    queue = service.q_repo.get_by_id(queue_id)
    if not queue:
        raise HTTPException(status_code=404, detail="Чергу не знайдено")

    user_id = request.cookies.get("user_id")
    my_pos = None
    if user_id:
        try:
            my_pos = service.get_my_position(queue_id, int(user_id))
        except:
            my_pos = None

    return templates.TemplateResponse(
        request=request,
        name="queue_view.html",
        context={"queue": queue, "my_pos": my_pos, "user_id": int(user_id) if user_id else None}
    )

@router.post("/queues/{queue_id}/join")
def join(queue_id: int, request: Request, service: QueueService = Depends(get_service)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    try:
        service.join_queue(queue_id, int(user_id))
        return responses.RedirectResponse(url=f"/queues/{queue_id}", status_code=303)
    except QueueBaseException as e:
        return responses.RedirectResponse(url=f"/queues/{queue_id}?error={e.message}", status_code=303)

@router.post("/queues/{queue_id}/next")
def call_next(queue_id: int, request: Request, service: QueueService = Depends(get_service)):
    user_id = request.cookies.get("user_id")
    try:
        service.call_next(queue_id, int(user_id))
        return responses.RedirectResponse(url=f"/queues/{queue_id}", status_code=303)
    except QueueBaseException as e:
        return responses.RedirectResponse(url=f"/queues/{queue_id}?error={e.message}", status_code=303)


@router.post("/queues/{queue_id}/close")
def close_queue(queue_id: int, request: Request, service: QueueService = Depends(get_service)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    try:
        service.close_registration(queue_id, int(user_id))
        return responses.RedirectResponse(url=f"/queues/{queue_id}", status_code=303)
    except QueueBaseException as e:
        return responses.RedirectResponse(url=f"/queues/{queue_id}?error={e.message}", status_code=303)

@router.post("/queues/{queue_id}/remove/{user_to_remove_id}")
def remove_user(queue_id: int, user_to_remove_id: int, request: Request, service: QueueService = Depends(get_service)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    try:
        service.remove_user_from_queue(queue_id, user_to_remove_id, int(user_id))
        return responses.RedirectResponse(url=f"/queues/{queue_id}", status_code=303)
    except QueueBaseException as e:
        return responses.RedirectResponse(url=f"/queues/{queue_id}?error={e.message}", status_code=303)

@router.post("/queues/{queue_id}/remove_by_select")
def remove_user_by_select(
        queue_id: int,
        request: Request,
        user_to_remove_id: int = Form(...),
        service: QueueService = Depends(get_service)
):
    """Обробник для видалення через випадаючий список"""
    user_id = request.cookies.get("user_id")
    if not user_id:
        return responses.RedirectResponse(url="/login", status_code=303)

    try:
        service.remove_user_from_queue(queue_id, user_to_remove_id, int(user_id))
        return responses.RedirectResponse(url=f"/queues/{queue_id}", status_code=303)
    except QueueBaseException as e:
        return responses.RedirectResponse(url=f"/queues/{queue_id}?error={e.message}", status_code=303)