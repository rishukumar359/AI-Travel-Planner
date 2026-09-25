from app.graph.state import TravelState


def transport_agent(state: TravelState):

    options = []

    for flight in state.get("flights", []):
        options.append(("flight", flight))

    for train in state.get("trains", []):
        options.append(("train", train))

    for bus in state.get("buses", []):
        options.append(("bus", bus))

    best_mode, best_option = min(
        options,
        key=lambda x: x[1]["price"]
    )
    print(best_mode,best_option)
    return {
        "best_transport_mode": best_mode,
        "best_transport": best_option,
        "transport_cost": best_option["price"],
        "transport_reason": "Selected based on lowest cost."
    }