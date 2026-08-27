from fastapi import FastAPI
from app.Routers import auth,habits,logs,insights
from app import models
from app.database import engine
from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded



models.base.metadata.create_all(bind=engine)


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(insights.router)
app.include_router(logs.router)
app.include_router(auth.router)
app.include_router(habits.router)
