from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)



@router.get("/x/")
async def x(request: Request):

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request
        }
    )