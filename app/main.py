from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import accounts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zerohertz's Auth API")

origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
