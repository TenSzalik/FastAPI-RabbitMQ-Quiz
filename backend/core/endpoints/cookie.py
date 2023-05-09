from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/cookie",
    tags=["cookie"],
    responses={404: {"description": "Not found"}},
)


@router.get("/set/")
def set_cookie():
    key = uuid4().hex
    content = {"queue": key}
    response = JSONResponse(content=content)
    response.set_cookie(
        key="queue",
        value=key,
        domain="localhost",
        path="/",
        secure=False,
        httponly=False,
    )
    return response
