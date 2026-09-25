from app.graph.state import TravelState


def search_trains(state: TravelState):

    print("Searching trains...")

    return {
        "trains": [
            {
                "train": "Demo Express",
                "price": 1800,
                "duration": "28h"
            }
        ]
    }