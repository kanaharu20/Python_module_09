#! /usr/bin/env python3
from enum import enum
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class ContactType(enum):
    

class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received:str | None = Field(max_length=500)
    is_verified:bool = False
    @model_validator(mode="after")
    def 