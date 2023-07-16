import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.endpoints import quiz, queue, token, user
from core.utils.load_simple_db import load_simple_db
from core.models.database import SessionLocal
from alembic.config import Config
from alembic import command

migrate_and_load_db = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(quiz.router)
app.include_router(queue.router)
app.include_router(token.router)
app.include_router(user.router)

if __name__ == "__main__":
    if migrate_and_load_db is True:
        try:
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            load_simple_db(SessionLocal())
        except Exception:
            pass

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
