from app.graph.state import TravelState


def route_after_validation(state: TravelState):

    missing_fields = state.get(
        "missing_fields",
        []
    )

    if missing_fields:
        return "clarification"

    return "transport_search"