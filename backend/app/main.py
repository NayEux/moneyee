from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import Base, engine
from .api import auth, securities, ai, portfolio, preferences

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(securities.router)
app.include_router(ai.router)
app.include_router(portfolio.router)
app.include_router(preferences.router)


@app.get("/")
def root():
    return {"status": "ok"}
