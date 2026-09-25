from langgraph.types import interrupt

from app.graph.state import TravelState


def clarification_agent(state: TravelState):

    print("\n")
    print("=" * 70)
    print("🙋 HUMAN CLARIFICATION")
    print("=" * 70)

    question = state.get(
        "clarification_question",
        "Please provide the missing information."
    )

    missing_fields = state.get(
        "missing_fields",
        []
    )

    print("\n❓ QUESTION:")
    print(question)

    print("\n⏸️ GRAPH PAUSED - WAITING FOR USER")

    # ======================================================
    # PAUSE GRAPH
    # ======================================================

    user_answer = interrupt({
        "question": question,
        "missing_fields": missing_fields
    })

    print("\n👤 USER CLARIFICATION:")
    print(user_answer)

    # ======================================================
    # RETURN USER ANSWER
    # ======================================================

    return {
        "user_clarification": user_answer
    }