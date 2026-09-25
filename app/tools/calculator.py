from app.graph.state import TravelState


def calculate_budget(state: TravelState):

    transport_costs = []

    for flight in state.get("flights", []):
        transport_costs.append(flight["price"])

    for train in state.get("trains", []):
        transport_costs.append(train["price"])

    for bus in state.get("buses", []):
        transport_costs.append(bus["price"])

    best_transport_cost = min(transport_costs)

    hotels = state.get("hotels", [])

    hotel_cost = (
        hotels[0]["price_per_night"] * state["duration_days"]
        if hotels
        else 0
    )

    total = best_transport_cost + hotel_cost

    return {
        "total_budget": total,
        "budget": {
            "transport": best_transport_cost,
            "hotel": hotel_cost,
            "total": total
        }
    }