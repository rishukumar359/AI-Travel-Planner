# from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.memory import InMemorySaver

# from app.graph.state import TravelState

# from app.agents.planner import planner_agent
# from app.agents.validator import validate_trip
# from app.agents.clarification import clarification_agent
# from app.agents.transport import transport_agent
# from app.agents.itinerary import itinerary_agent

# from app.tools.flight import search_flights
# from app.tools.train import search_trains
# from app.tools.bus import search_buses
# from app.tools.hotel import search_hotels
# from app.tools.calculator import calculate_budget


# # ==========================================
# # Graph
# # ==========================================

# builder = StateGraph(TravelState)


# # ==========================================
# # Nodes
# # ==========================================

# builder.add_node("planner", planner_agent)

# builder.add_node("validator", validate_trip)

# builder.add_node(
#     "clarification",
#     clarification_agent
# )

# builder.add_node(
#     "flight_search",
#     search_flights
# )

# builder.add_node(
#     "train_search",
#     search_trains
# )

# builder.add_node(
#     "bus_search",
#     search_buses
# )

# builder.add_node(
#     "transport_agent",
#     transport_agent
# )

# builder.add_node(
#     "hotel_search",
#     search_hotels
# )

# builder.add_node(
#     "budget_calculator",
#     calculate_budget
# )

# builder.add_node(
#     "itinerary_agent",
#     itinerary_agent
# )


# # ==========================================
# # START
# # ==========================================

# builder.add_edge(
#     START,
#     "planner"
# )


# # ==========================================
# # Planner → Validator
# # ==========================================

# builder.add_edge(
#     "planner",
#     "validator"
# )


# # ==========================================
# # Validation Router
# # ==========================================

# def route_after_validation(state: TravelState):

#     missing_fields = state.get(
#         "missing_fields",
#         []
#     )

#     if missing_fields:
#         return "clarification"

#     return "flight_search"


# builder.add_conditional_edges(
#     "validator",
#     route_after_validation,
#     {
#         "clarification": "clarification",
#         "flight_search": "flight_search"
#     }
# )


# # ==========================================
# # Transport
# # ==========================================

# builder.add_edge(
#     "flight_search",
#     "transport_agent"
# )


# # ==========================================
# # Continue
# # ==========================================

# builder.add_edge(
#     "transport_agent",
#     "hotel_search"
# )

# builder.add_edge(
#     "hotel_search",
#     "budget_calculator"
# )

# builder.add_edge(
#     "budget_calculator",
#     "itinerary_agent"
# )


# # ==========================================
# # END
# # ==========================================

# builder.add_edge(
#     "itinerary_agent",
#     END
# )

# # builder.add_edge(
# #     "clarification",
# #     END
# # )


# # ==========================================
# # CHECKPOINTER
# # ==========================================

# checkpointer = InMemorySaver()


# # ==========================================
# # COMPILE
# # ==========================================

# graph = builder.compile(
#     checkpointer=checkpointer
# )

from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.memory import InMemorySaver
from app.graph.checkpointer import checkpointer

from app.graph.state import TravelState

from app.agents.planner import planner_agent
from app.agents.validator import validate_trip
from app.agents.clarification import clarification_agent
from app.agents.transport import transport_agent
from app.agents.itinerary import itinerary_agent

from app.tools.flight import search_flights
from app.tools.train import search_trains
from app.tools.bus import search_buses
from app.tools.hotel import search_hotels
from app.tools.calculator import calculate_budget


# ============================================================
# GRAPH
# ============================================================

builder = StateGraph(TravelState)


# ============================================================
# NODES
# ============================================================

builder.add_node("planner", planner_agent)

builder.add_node("validator", validate_trip)

builder.add_node(
    "clarification",
    clarification_agent
)

builder.add_node(
    "flight_search",
    search_flights
)

builder.add_node(
    "train_search",
    search_trains
)

builder.add_node(
    "bus_search",
    search_buses
)

builder.add_node(
    "transport_agent",
    transport_agent
)

builder.add_node(
    "hotel_search",
    search_hotels
)

builder.add_node(
    "budget_calculator",
    calculate_budget
)

builder.add_node(
    "itinerary_agent",
    itinerary_agent
)


# ============================================================
# START
# ============================================================

builder.add_edge(
    START,
    "planner"
)


# ============================================================
# PLANNER → VALIDATOR
# ============================================================

builder.add_edge(
    "planner",
    "validator"
)


# ============================================================
# VALIDATION ROUTER
# ============================================================

def route_after_validation(state: TravelState):

    missing_fields = state.get(
        "missing_fields",
        []
    )

    print("\n")
    print("=" * 70)
    print("🔀 VALIDATION ROUTER")
    print("=" * 70)

    print("Missing fields:", missing_fields)

    # --------------------------------------------------------
    # Missing information
    # --------------------------------------------------------

    if missing_fields:

        print("➡️ Routing to clarification")

        return "clarification"

    # --------------------------------------------------------
    # Complete information
    # --------------------------------------------------------

    print("➡️ Routing to parallel transport search")

    return "parallel_search"


# ============================================================
# VALIDATOR → ROUTER
# ============================================================

builder.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "clarification": "clarification",

        "parallel_search": "parallel_search"
    }
)


# ============================================================
# PARALLEL SEARCH DISPATCHER
# ============================================================

def parallel_search(state: TravelState):

    print("\n")
    print("=" * 70)
    print("🚀 PARALLEL SEARCH DISPATCHER")
    print("=" * 70)

    print("Starting:")
    print("   ✈️ Flight search")
    print("   🚆 Train search")
    print("   🚌 Bus search")

    return {}


builder.add_node(
    "parallel_search",
    parallel_search
)


# ============================================================
# DISPATCHER → PARALLEL SEARCHES
# ============================================================

builder.add_edge(
    "parallel_search",
    "flight_search"
)

builder.add_edge(
    "parallel_search",
    "train_search"
)

builder.add_edge(
    "parallel_search",
    "bus_search"
)


# ============================================================
# PARALLEL SEARCHES → TRANSPORT AGENT
# ============================================================

builder.add_edge(
    "flight_search",
    "transport_agent"
)

builder.add_edge(
    "train_search",
    "transport_agent"
)

builder.add_edge(
    "bus_search",
    "transport_agent"
)


# ============================================================
# TRANSPORT → HOTEL
# ============================================================

builder.add_edge(
    "transport_agent",
    "hotel_search"
)


# ============================================================
# HOTEL → BUDGET
# ============================================================

builder.add_edge(
    "hotel_search",
    "budget_calculator"
)


# ============================================================
# BUDGET → ITINERARY
# ============================================================

builder.add_edge(
    "budget_calculator",
    "itinerary_agent"
)


# ============================================================
# ITINERARY → END
# ============================================================

builder.add_edge(
    "itinerary_agent",
    END
)


# ============================================================
# HUMAN CLARIFICATION
# ============================================================
#
# clarification_agent uses interrupt().
#
# After user provides the answer, the graph resumes
# and goes back to planner.
#
# ============================================================

builder.add_edge(
    "clarification",
    "planner"
)


# ============================================================
# CHECKPOINTER
# ============================================================

# checkpointer = InMemorySaver()


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile(
    checkpointer=checkpointer
)