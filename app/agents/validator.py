from app.graph.state import TravelState


REQUIRED_FIELDS = [
    "origin",
    "destination",
    "duration_days",
    "budget_limit"
]


def validate_trip(state: TravelState):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        value = state.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    print(
        "Missing fields:",
        missing_fields
    )

    if missing_fields:

        return {
            "missing_fields": missing_fields,
            "clarification_question": (
                "I need some more information "
                "to plan your trip: "
                + ", ".join(missing_fields)
            )
        }

    return {
        "missing_fields": [],
        "clarification_question": ""
    }