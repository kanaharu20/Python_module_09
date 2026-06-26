#! /usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime


class Rank(Enum):
    CADET: str = "cadet"
    OFFICER: str = "officer"
    LIEUTENANT: str = "lieutenant"
    CAPTAIN: str = "captain"
    COMMANDER: str = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_id(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission Id must start with 'M'")
        return self

    @model_validator(mode="after")
    def validate_crew_mem(self) -> "SpaceMission":
        list_commander: list[CrewMember] = []
        list_captain: list[CrewMember] = []
        for mem in self.crew:
            if mem.rank == Rank.COMMANDER:
                list_commander.append(mem)
            elif mem.rank == Rank.CAPTAIN:
                list_captain.append(mem)
        if len(list_commander) < 1 and len(list_captain) < 1:
            raise ValueError(
                "Mission must have at least "
                "one Commander or Captain")
        return self

    @model_validator(mode="after")
    def validate_long_mission(self) -> "SpaceMission":
        if self.duration_days > 365:
            num_experienced: int = 0
            for mem in self.crew:
                if mem.years_experience > 5:
                    num_experienced += 1
            if num_experienced/len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need"
                    " 50% experienced crew (5+ years)")
        return self

    @model_validator(mode="after")
    def validate_status(self) -> "SpaceMission":
        for mem in self.crew:
            if not mem.is_active:
                raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    valid_crews = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=42,
            specialization="Mission Command",
            years_experience=15,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=5,
        ),
    ]

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2026, 6, 17, 14, 0, 0),
        duration_days=900,
        crew=valid_crews,
        budget_millions=2500.0,
    )
    print("Valid mission created:")

    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")

    print("Crew members:")
    for mem in valid_mission.crew:
        print(
            f"- {mem.name} ({mem.rank.value}) "
            f"- {mem.specialization}"
        )

    print("\n=========================================")

    invalid_crews = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.CADET,
            age=42,
            specialization="Mission Command",
            years_experience=15,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=5,
        ),
    ]
    try:
        _ = SpaceMission(
            mission_id="M2143_CA",
            mission_name="Centaur Alpha Exploring",
            destination="Centaur Alpha",
            launch_date=datetime.now(),
            duration_days=2000,
            crew=invalid_crews,
            budget_millions=100.0
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            ctx = error.get('ctx', {})
            msg = str(ctx['error']) if 'error' in ctx else error['msg']
            print(msg)


if __name__ == "__main__":
    main()
