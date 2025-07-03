from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import re


def format_error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "errors": [message],
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return format_error_response(exc.detail, exc.status_code)


async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = [e["msg"] for e in exc.errors()]
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": errors},
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig).lower()

    # Try to extract the field name using a regex pattern
    # This works for PostgreSQL and similar error formats
    match = re.search(r'key \((.*?)\)=', error_message)
    if match:
        field_name = match.group(1)
        message = f"Field '{field_name}' must be unique."
    else:
        message = "A database integrity error occurred."

    return format_error_response(message, status_code=400)


async def generic_exception_handler(request: Request, exc: Exception):
    return format_error_response("An unexpected error occurred.", status_code=500)
