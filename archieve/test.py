import json

from app.llm.client import get_llm


# ==========================================
# Get LLM
# ==========================================

llm = get_llm()


# ==========================================
# Same query as planner
# ==========================================

query = "I want to travel to Goa for 4 days"


previous_state = {
    "origin": None,
    "destination": None,
    "duration_days": None,
    "budget_limit": None,
    "transport_preference": None,
}


# ==========================================
# Simple prompt
# ==========================================

prompt = f"""
Extract travel information from the user message.

EXISTING STATE:
{json.dumps(previous_state, indent=2)}

USER MESSAGE:
{query}

Return ONLY valid JSON.

Required format:

{{
    "origin": null,
    "destination": null,
    "duration_days": null,
    "budget_limit": null,
    "transport_preference": "any"
}}

Rules:

- Keep existing values.
- Extract values from the user message.
- Do not guess missing values.
- Missing values must be null.
- duration_days must be an integer.
- budget_limit must be a number.
- transport_preference must be flight, train, bus, or any.
- Do not return markdown.
- Do not return explanations.
"""


# ==========================================
# Call LLM
# ==========================================

print("\n" + "=" * 70)
print("🧪 LLM STANDALONE TEST")
print("=" * 70)

print("\n📤 PROMPT:")
print(prompt)

print("\n🤖 CALLING LLM...")

response = llm.invoke(prompt)


# ==========================================
# Inspect response
# ==========================================

print("\n📦 RESPONSE TYPE:")
print(type(response))

print("\n🤖 RAW RESPONSE:")
print(response.content)

print("\n🔍 RAW RESPONSE REPR:")
print(repr(response.content))

print("\n📏 RESPONSE LENGTH:")
print(len(response.content))


# ==========================================
# Try JSON parsing
# ==========================================

try:

    data = json.loads(response.content.strip())

    print("\n✅ JSON PARSING SUCCESSFUL")
    print(data)

except json.JSONDecodeError as e:

    print("\n❌ JSON PARSING FAILED")
    print("Error:", e)

print("\n" + "=" * 70)
print("🏁 TEST FINISHED")
print("=" * 70)