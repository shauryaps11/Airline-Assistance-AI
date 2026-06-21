import json
from openai import OpenAI
from backend.config import settings

_client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are an intent classifier for SkyAssist, an airline customer support AI.

Classify the user message into exactly one of:
- price_inquiry      : asking about ticket prices, fares, or costs to a destination
- destination_image  : wants to see a destination, travel inspiration, "show me X", "what does X look like"
- booking_info       : seat availability, how to book, confirmation codes, check-in
- general_faq        : baggage rules, flight policies, hours, cancellation policy
- escalation         : complaint, refund request, anger, wants a supervisor

Return ONLY valid JSON — no markdown, no explanation:
{"intent": "<label>", "confidence": <0.0-1.0>, "params": {"destination_city": "<city or null>"}}

If no city is mentioned, set destination_city to null."""


def classify(message: str, memory_snippets: list[str] = None) -> dict:
    context = ""
    if memory_snippets:
        context = "\n\nRelevant conversation history:\n" + "\n---\n".join(memory_snippets)

    response = _client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Message: {message}{context}"}
        ],
        max_tokens=100,
        temperature=0,
    )
    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, KeyError):
        return {"intent": "general_faq", "confidence": 0.5, "params": {"destination_city": None}}
