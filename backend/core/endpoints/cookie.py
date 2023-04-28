from fastapi import Cookie, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
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


@router.get("/check/")
def check_cookie(queue: str = Cookie(None)):
    if not queue:
        return HTTPException(status_code=404, detail="Cookie not found")
    if queue:
        return HTTPException(status_code=200, detail="Cookie exist")
