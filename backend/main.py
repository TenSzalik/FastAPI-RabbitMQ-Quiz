from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.endpoints import quiz, queue, cookie, chart

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(quiz.router)
app.include_router(queue.router)
app.include_router(cookie.router)
app.include_router(chart.router)
