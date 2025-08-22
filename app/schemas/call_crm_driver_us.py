from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

# Shared properties
class CallCrmDUBase(BaseModel):
    user_from: str = None
    stamp_time: str = None
    status_call: str = None
    duration: str = None
    contact_id: str = None
    direction: str = None

# Properties to receive via API on creation
class CallCrmCreate(CallCrmDUBase):
    pass

class CallCrmUpdate(CallCrmDUBase):
    pass
class CallCrmInDb(CallCrmDUBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class CallCrmSesion(CallCrmDUBase):
    pass