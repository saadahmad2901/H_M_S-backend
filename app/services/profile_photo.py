import os
import shutil
import random
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

BASE_DIR = "uploads"
DOCTOR_DIR = os.path.join(BASE_DIR, "doctor")
PATIENT_DIR = os.path.join(BASE_DIR, "patient")

os.makedirs(DOCTOR_DIR, exist_ok=True)
os.makedirs(PATIENT_DIR, exist_ok=True)

def profile_photo(id: int, role: str, photo: UploadFile, db: Session) -> schemas.ProfilePhotoBase:
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    random_digits = random.randint(1000, 9999)
    safe_filename = os.path.basename(photo.filename)
    filename = f"{role}_{id}_{random_digits}-{safe_filename}"

    if role == "doctor":
        folder = DOCTOR_DIR
        user = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    elif role == "patient":
        folder = PATIENT_DIR
        user = db.query(models.Patient).filter(models.Patient.id == id).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid role: use 'doctor' or 'patient'")

    if not user:
        raise HTTPException(status_code=404, detail=f"{role.capitalize()} with ID {id} not found")

    # Save image
    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Store relative path in DB
    relative_path = os.path.join(role, filename).replace("\\", "/")
    user.photo = relative_path
    db.commit()
    db.refresh(user)

    return schemas.ProfilePhotoBase(photo=filepath)


def get_profile_photo(id:   int, role: str, db: Session):
    if role == "doctor":
        user = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    elif role == "patient":
        user = db.query(models.Patient).filter(models.Patient.id == id).first()

    else:
        raise HTTPException(status_code=400, detail="Invalid role: use 'doctor' or 'patient'")

    if not user or not user.photo:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    filepath = os.path.join(BASE_DIR, user.photo)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Profile photo file missing on server")

    with open(filepath, "rb") as f:
        photo_bytes = f.read()

    return photo_bytes, "image/jpeg"   # or detect based on file extension
