import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.models.schemas import UserSchema, UserInDB
from core.models.models import User
from core.models.database import get_database
from core.utils.get_hashed_password import get_hashed_password

SECRET_KEY = os.environ["SECRET_KEY"]

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserInDB)
def create_user(user: UserSchema, database: Session = Depends(get_database)):
    if user.key == SECRET_KEY:
        hashed_password = get_hashed_password(user.password)
        user = User(email=user.email, password=hashed_password)
        database.add(user)
        database.commit()
        return {"email": user.email, "hashed_password": hashed_password}
    raise HTTPException(status_code=401, detail="Key is incorrect")
