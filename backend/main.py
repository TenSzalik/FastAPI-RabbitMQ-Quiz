from fastapi import FastAPI
from core.endpoints import quiz, queue, cookie, chart

app = FastAPI()

app.include_router(quiz.router)
app.include_router(queue.router)
app.include_router(cookie.router)
app.include_router(chart.router)
