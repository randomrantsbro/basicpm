from fastapi import FastAPI
from .routes import users, tasks, events, notes, gemini

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(notes.router)
app.include_router(gemini.router)
