from fastapi import FastAPI
from db.database import Base, engine
from controllers.controllers import router as math_router
from controllers.frontend_controllers import router as frontend_router
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Math Microservice")
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(frontend_router)
app.include_router(math_router)
