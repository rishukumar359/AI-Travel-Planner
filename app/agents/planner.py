import json
import re

from app.graph.state import TravelState
from app.schemas.travel import TravelPlan
from app.llm.client import get_llm
import logging

logger = logging.getLogger(__name__)


# ============================================================
# LLM
# ============================================================

llm = get_llm()


# ============================================================
# JSON CLEANER
# ============================================================

def clean_json_response(content: str) -> str:
    """
    Clean LLM response and extract the JSON object.

    Handles:
        ```json
        {...}
        ```

    Also handles cases where the LLM adds
    extra text before/after the JSON.
    """

    if not content:
        raise ValueError("LLM returned an empty response.")

    content = content.strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    content = re.sub(
        r"^```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"^```\s*",
        "",
        content
    )

    content = re.sub(
        r"\s*```$",
        "",
        content
    )

    content = content.strip()

    # --------------------------------------------------------
    # Try to find JSON object
    # --------------------------------------------------------

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            f"No valid JSON object found in LLM response: {content}"
        )

    content = content[start:end + 1]

    return content.strip()


# ============================================================
# PLANNER AGENT
# ============================================================

def planner_agent(state: TravelState):


   # ========================================================
    # 1. CURRENT USER QUERY / CLARIFICATION
    # ========================================================

    query = state.get("user_query", "").strip()

    # If graph was resumed after human clarification,
    # use the clarification as the new user message.
    if state.get("user_clarification"):
        query = state["user_clarification"].strip()

    print("\n👤 CURRENT USER QUERY:")
    print(query)
    

    logger.info(
    "planner agent query",
    query
)

    if state.get("user_clarification"):
        logger.info("🔄 QUERY SOURCE: HUMAN CLARIFICATION")
    else:
        logger.info("🆕 QUERY SOURCE: INITIAL USER QUERY")

    if not query:
        raise ValueError("user_query is empty.")

    # ========================================================
    # 2. EXISTING / PREVIOUS STATE
    # ========================================================

    previous_state = {
        "origin": state.get("origin"),
        "destination": state.get("destination"),
        "duration_days": state.get("duration_days"),
        "budget_limit": state.get("budget_limit"),
        "transport_preference":
            state.get("transport_preference"),
    }

    logger.info("\n💾 EXISTING TRAVEL STATE:")
    logger.info(json.dumps(previous_state, indent=2))

    # ========================================================
    # 3. PROMPT
    # ========================================================

    prompt = f"""
You are a travel information extraction system.

Your job is to merge the existing travel state
with the new user message.

EXISTING STATE:
{json.dumps(previous_state, indent=2)}

NEW USER MESSAGE:
{query}

RULES:

1. Keep all existing values unless the user explicitly
   provides a new value.

2. Extract new information from the user message.

3. Never guess missing information.

4. Missing information must be null.

5. duration_days must be an integer or null.

6. budget_limit must be a number or null.

7. transport_preference must be one of:
   "flight", "train", "bus", "any"

8. Return exactly one JSON object.

9. Do NOT return markdown.

10. Do NOT return explanations.

11. Do NOT return text before or after the JSON.

OUTPUT FORMAT:

{{
  "origin": null,
  "destination": null,
  "duration_days": null,
  "budget_limit": null,
  "transport_preference": "any"
}}
"""


    # ========================================================
    # 4. CALL LLM
    # ========================================================

    logger.info("\n🤖 Calling Hugging Face LLM...")

    try:
        response = llm.invoke(prompt)

    except Exception as e:

        logger.info("\n❌ LLM CALL FAILED")
        logger.info("Error:", repr(e))

        raise RuntimeError(
            "Planner LLM call failed."
        ) from e

    # ========================================================
    # 5. RAW RESPONSE
    # ========================================================

    content = response.content

    # ========================================================
    # 6. CLEAN JSON
    # ========================================================

    try:

        cleaned_content = clean_json_response(content)

    except Exception as e:

        logger.info("\n❌ JSON CLEANING FAILED")
        logger.info("Error:", e)

        raise ValueError(
            f"Unable to extract JSON from LLM response: {content}"
        ) from e

    print("\n🧹 CLEANED JSON:")
    print("-" * 70)
    print(cleaned_content)
    print("-" * 70)

    # ========================================================
    # 7. PARSE JSON
    # ========================================================

    try:

        data = json.loads(cleaned_content)

    except json.JSONDecodeError as e:

        print("\n❌ JSON PARSING FAILED")
        print("Error:", e)
        print("Response:", repr(content))
        print("Cleaned:", repr(cleaned_content))

        raise ValueError(
            f"LLM returned invalid JSON: {cleaned_content}"
        ) from e

    print("\n✅ PARSED PLANNER DATA:")
    print(json.dumps(data, indent=2))

    # ========================================================
    # 8. ENSURE DICT
    # ========================================================

    if not isinstance(data, dict):

        raise ValueError(
            f"Planner output must be a JSON object, got: {type(data)}"
        )

    # ========================================================
    # 9. SAFETY MERGE
    # ========================================================
    #
    # This is important.
    #
    # Even though the prompt tells the LLM to preserve
    # existing state, we don't blindly trust the LLM.
    #
    # If an old value exists and the LLM accidentally returns
    # null, keep the old value.
    #
    # ========================================================

    fields = [
        "origin",
        "destination",
        "duration_days",
        "budget_limit",
        "transport_preference",
    ]

    merged_data = {}

    for field in fields:

        new_value = data.get(field)
        old_value = previous_state.get(field)

        if new_value is None and old_value is not None:
            merged_data[field] = old_value

        else:
            merged_data[field] = new_value

    # ========================================================
    # 10. DEFAULT TRANSPORT
    # ========================================================

    if not merged_data.get("transport_preference"):
        merged_data["transport_preference"] = "any"

    # ========================================================
    # 11. PYDANTIC VALIDATION
    # ========================================================

    print("\n🔍 VALIDATING PLANNER OUTPUT...")

    try:

        travel_plan = TravelPlan.model_validate(
            merged_data
        )

    except Exception as e:

        print("\n❌ PYDANTIC VALIDATION FAILED")
        print("Error:", e)
        print("Data:", merged_data)

        raise ValueError(
            f"Invalid planner output: {merged_data}"
        ) from e

    # ========================================================
    # 12. CREATE UPDATED STATE
    # ========================================================

    result = {
        "origin": travel_plan.origin,
        "destination": travel_plan.destination,
        "duration_days": travel_plan.duration_days,
        "budget_limit": travel_plan.budget_limit,
        "transport_preference":
            travel_plan.transport_preference,
    }

    # ========================================================
    # 13. STATE DIFF DEBUG
    # ========================================================

    print("\n📊 STATE CHANGES:")

    for field in fields:

        old_value = previous_state.get(field)
        new_value = result.get(field)

        if old_value != new_value:

            print(
                f"   🔄 {field}: "
                f"{old_value!r} → {new_value!r}"
            )

        else:

            print(
                f"   ➡️ {field}: "
                f"{new_value!r} (unchanged)"
            )

    # ========================================================
    # 14. FINAL RESULT
    # ========================================================

    print("\n📤 PLANNER RETURNING:")
    print("-" * 70)
    print(json.dumps(result, indent=2))
    print("-" * 70)

    print("=" * 70)
    print("✅ PLANNER COMPLETED")
    print("=" * 70)
    print()

    return result

