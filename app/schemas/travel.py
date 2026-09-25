from typing import Literal

from pydantic import BaseModel, Field


class TravelPlan(BaseModel):

    origin: str | None = Field(
        default=None,
        description="Starting city"
    )

    destination: str | None = Field(
        default=None,
        description="Destination city"
    )

    duration_days: int | None = Field(
        default=None,
        description="Number of travel days"
    )

    budget_limit: float | None = Field(
        default=None,
        description="Maximum budget in INR"
    )

    transport_preference: Literal[
        "flight",
        "train",
        "bus",
        "any"
    ] = "any"