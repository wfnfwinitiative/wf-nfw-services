from typing import List, Optional
from datetime import datetime

from openai import BaseModel

class ReportFilterRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    driver_ids: Optional[List[int]] = None  
    hunger_spot_ids: Optional[List[int]] = None 

    donor_id: Optional[int] = None
    status_id: Optional[int] = None