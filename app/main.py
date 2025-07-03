from fastapi import FastAPI
from app.core import settings
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.core import custom_exception_handler
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routes import patient_router, doctor_router, appointment_router,dropdown_router,visit_router,service_router,visit_service_router,user_router
from fastapi_pagination import add_pagination

# Create the FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
)
add_pagination(app)

origins = [
    "http://localhost:3000",  # Adjust this to your frontend URL
]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the API router
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(patient_router, prefix=settings.API_V1_STR)
app.include_router(doctor_router, prefix=settings.API_V1_STR)
app.include_router(appointment_router, prefix=settings.API_V1_STR)
app.include_router(visit_router, prefix=settings.API_V1_STR)
app.include_router(service_router, prefix=settings.API_V1_STR)
app.include_router(visit_service_router, prefix=settings.API_V1_STR)
app.include_router(dropdown_router, prefix=settings.API_V1_STR)


# Register your exception handlers
app.add_exception_handler(StarletteHTTPException, custom_exception_handler.http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_exception_handler.validation_exception_handler)
app.add_exception_handler(IntegrityError, custom_exception_handler.integrity_error_handler)
app.add_exception_handler(Exception, custom_exception_handler.generic_exception_handler)


# Create the database tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
def shutdown_event():
    # Here you can add any cleanup code if needed
    pass


# Define a root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the WellNest API!"}


# This is the main entry point for the FastAPI application.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
# To run the application, use the command:
# uvicorn app.main:app --reload
# This will start the FastAPI server with live reloading enabled.
# Make sure to adjust the import paths based on your project structure.
# The above code sets up a FastAPI application with CORS middleware, includes an API router, and initializes the database tables on startup.
# It also defines a root endpoint that returns a welcome message.
# Ensure you have the necessary dependencies installed:
# pip install fastapi uvicorn sqlalchemy pydantic
