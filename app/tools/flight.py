from app.graph.state import TravelState


def search_flights(state: TravelState):

    print("Searching flights...")

    return {
        "flights": [
            {
                "airline": "Demo Airways",
                "price": 6500,
                "duration": "3h"
            }
        ]
    }