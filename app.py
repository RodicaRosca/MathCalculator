from fastapi import FastAPI
#from db.database import Base, engine
from controllers.controllers import router as math_router
from controllers.frontend_controllers import router as frontend_router

# Create tables on startup
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Math Microservice")

app.include_router(frontend_router)
app.include_router(math_router)
