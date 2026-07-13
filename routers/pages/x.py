from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)



@router.get("/x/")
async def x(
    request: Request
):

    admin_id = request.session.get(
        "admin_id"
    )


    if not admin_id:

        return RedirectResponse(
            "/"
        )


    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request
        }
    )