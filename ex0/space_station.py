#!/usr/bin/env python3
from pydantic import BaseModel, model_validator, Field, ValidationError
from datetime import datetime

class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    
    valid_ss = SpaceStation(
        station_id = "ISS001",
        name = "International Space Station",
        crew_size = 6,
        power_level = 85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2026, 6, 25, 12, 6, 30),
        notes= "The Earth is blue",
        is_operational=True
        )
    print("Valid station created:")
    print(f"ID: {valid_ss.station_id}")
    print(f"Name: {valid_ss.name}")
    print(f"Crew: {valid_ss.crew_size}")
    print(f"Power: {valid_ss.power_level}")
    print(f"Oxygen: {valid_ss.oxygen_level}")
    print(f"last maintenance datetime: {valid_ss.last_maintenance}")
    if valid_ss.notes:
        print(f"notes: {valid_ss.notes}")
    if valid_ss.is_operational:
        print("Status: Operational")
    else:
        print("Status: non-Oparational")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        invalid_ss = SpaceStation(
            station_id = "ISS001",
            name = "International Space Station",
            crew_size = 21,
            power_level = 85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 6, 25, 12, 6, 30),
            notes= "The Earth is blue",
            is_operational=True
            )
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
