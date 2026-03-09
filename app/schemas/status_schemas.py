from pydantic import BaseModel
from datetime import datetime


class StatusCreate(BaseModel):
    status_name: str


class StatusUpdate(BaseModel):
    status_name: str


class StatusRead(BaseModel):
    status_id: int
    status_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
