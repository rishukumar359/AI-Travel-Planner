from app.graph.state import TravelState


def itinerary_agent(state: TravelState):

    return {
        "itinerary": {
            "destination": state["destination"],
            "duration": state["duration_days"],
            "transport": state["best_transport"],
            "hotel": state.get("hotels", [None])[0],
            "estimated_cost": state["total_budget"]
        }
    }