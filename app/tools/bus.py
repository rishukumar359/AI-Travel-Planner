from app.graph.state import TravelState


def search_buses(state: TravelState):

    print("Searching buses...")

    return {
        "buses": [
            {
                "bus": "Demo Sleeper",
                "price": 2200,
                "duration": "24h"
            }
        ]
    }