from pydantic import BaseModel

class DropDownSchema(BaseModel):
    value: int|str
    label: str

class DropDownList(BaseModel):
    items: list[DropDownSchema]
