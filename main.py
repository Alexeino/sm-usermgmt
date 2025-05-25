from contextlib import asynccontextmanager
from fastapi import FastAPI
from settings.config import settings
from db.session import sessionmanager
from api.v1.users.routers import user_router

def init_app(init_db=True):
    lifespan = None
    
    if init_db:
        sessionmanager.init(settings.get_db_url())
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(title=settings.PROJECT_TITLE, lifespan=lifespan)
    server.include_router(user_router,prefix="/api/v1")
    return server

server = init_app()