from app.graph.state import TravelState


def search_hotels(state: TravelState):

    print("Searching hotels...")

    return {
        "hotels": [
            {
                "name": "Demo Hotel",
                "price_per_night": 2500,
                "rating": 4.2
            }
        ]
    }