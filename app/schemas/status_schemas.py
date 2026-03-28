from pydantic import BaseModel


class StatusBase(BaseModel):
    class Config:
        from_attributes = True


class StatusRead(StatusBase):
    status_id: int
    status_name: str