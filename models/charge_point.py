from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ChargePointModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    id: Optional[str] = None
    serial_number: Optional[str] = Field(None, alias="serialNumber")
