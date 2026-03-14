from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# =====================================================
# BASE CONFIG
# =====================================================


class FeatureFlagBaseSchema(BaseModel):
    class Config:
        from_attributes = True  # Pydantic v2 compatible


# =====================================================
# FEATURE FLAGS
# =====================================================


class FeatureFlagCreate(BaseModel):
    feature_flag_name: str
    enabled: bool = False


class FeatureFlagUpdate(BaseModel):
    enabled: bool


class FeatureFlagRead(FeatureFlagBaseSchema):
    id: int
    feature_flag_name: str
    enabled: bool
    created_at: datetime
    updated_at: datetime
