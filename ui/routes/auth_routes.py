from fastapi import APIRouter, Depends, Request, Form, responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dal.database import get_db
from dal.repositories import UserRepository, QueueRepository, QueueEntryRepository
from bll.services import QueueService, AuthService
from bll.exceptions import QueueBaseException

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="ui/templates")

def get_service(db: Session = Depends(get_db)):
    return QueueService(UserRepository(db), QueueRepository(db), QueueEntryRepository(db))

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@router.post("/register")
def register_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        full_name: str = Form(None),
        age: int = Form(None),
        service: QueueService = Depends(get_service)
):
    try:
        service.register_user(username=username, password=password, full_name=full_name, age=age)
        return responses.RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(request=request, name="register.html", context={"error": str(e)})

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login")
def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
        service: QueueService = Depends(get_service)
):
    user = service.u_repo.get_by_username(username)

    if user and AuthService.verify_password(password, user.hashed_password):
        response = responses.RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(user.id))
        return response

    return templates.TemplateResponse(request=request, name="login.html", context={"error": "Невірний логін або пароль"})

@router.get("/logout")
def logout():
    response = responses.RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_id")
    return response