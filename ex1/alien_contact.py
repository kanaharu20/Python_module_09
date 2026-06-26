#! /usr/bin/env python3
from enum import enum
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class ContactType(enum):
    radio: str = "radio"
    visual: str = "visual"
    physical: str = "physical"
    telepathic: str = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def contact_validate(self) -> self:
        if not self.contact_id.startswith("AC"):
            raise ValidationError("Contact ID must ")
        elif self.contact_type == ContactType.physical:
            if not self.is_verified:
                raise ValidationError
        elif self.contact_type == ContactType.telepathic:
            if self.witness_count < 3:
                raise ValidationError
        elif self.signal_strength > 7.0:
            if not self.message_received:
                raise ValidationError
        return self
