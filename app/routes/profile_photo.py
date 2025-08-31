from fastapi import APIRouter, Depends, UploadFile, File, Form,Path,Response,Query
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import schemas, services

router = APIRouter(prefix="/profile-photo", tags=["profile"])

@router.put("/", response_model=APIResponse[schemas.ProfilePhotoBase])
def upload_profile_photo(
    id: int = Form(...),
    role: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = services.profile_photo(id=id, role=role, photo=photo, db=db)
    return APIResponse(data=result, message="Photo uploaded successfully")

@router.get("/")
def get_profile_photo(
    id: int = Query(...),
    role: str = Query(...),
    db: Session = Depends(get_db)
):
    photo_bytes, content_type = services.get_profile_photo(id=id, role=role, db=db)
    return Response(content=photo_bytes, media_type=content_type)

