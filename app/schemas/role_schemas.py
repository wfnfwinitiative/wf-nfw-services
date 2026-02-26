from pydantic import BaseModel


class RoleBase(BaseModel):
    class Config:
        from_attributes = True


class RoleRead(RoleBase):
    role_id: int
    role_name: str