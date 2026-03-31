from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ReportFilterRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    driver_ids: Optional[List[int]] = None
    hunger_spot_ids: Optional[List[int]] = None
    vehicle_ids: Optional[List[int]] = None
    donor_ids: Optional[List[int]] = None
    status_ids: Optional[List[int]] = None  # 🔥 ADD THIS