from fastapi import FastAPI
from app.Routers import auth,habits,logs,insights
from app import models
from app.database import engine
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded



models.base.metadata.create_all(bind=engine)


app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)


app.include_router(insights.router)
app.include_router(logs.router)
app.include_router(auth.router)
app.include_router(habits.router)
