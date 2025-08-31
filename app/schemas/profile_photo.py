from typing import  Optional

from pydantic import BaseModel

class ProfilePhotoBase(BaseModel):
    photo: Optional[str] = None



