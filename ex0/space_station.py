#!/usr/bin/env python3
from pydantic import BaseModel, model_validator, Field
from typing import Optional


class SpaceStationData(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    @model_validator(mode="after")
    def validate_station_id(self) ->
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance:
    is_operational: bool = Field(delault = True)
    notes: str | None = None
    @




def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
