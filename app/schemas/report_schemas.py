from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportFilterRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    driver_id: Optional[int] = None
    hunger_spot_id: Optional[int] = None
    donor_id: Optional[int] = None
    status_id: Optional[int] = None