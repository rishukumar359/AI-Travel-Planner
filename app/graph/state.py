from typing import TypedDict
from typing import Literal

class TravelState(TypedDict, total=False):

    # User
    user_query: str

    # Planner
    origin: str | None
    destination: str | None
    duration_days: int | None
    budget_limit: float | None
    transport_preference: Literal[
    "flight",
    "train",
    "bus",
    "any"
] | None

    # Validation / HITL
    missing_fields: list[str]
    clarification_question: str
    user_clarification: str

    # Search
    flights: list
    trains: list
    buses: list
    hotels: list

    # Transport
    best_transport_mode: str | None
    best_transport: dict | None
    transport_cost: float | None
    transport_reason: str | None

    # Budget
    budget: dict | None
    total_budget: float | None

    # Final
    itinerary: dict | None