from openai import OpenAI
from backend.config import settings

_client = OpenAI(api_key=settings.openai_api_key)

ESCALATION_KEYWORDS = {"refund", "supervisor", "complaint", "unacceptable", "terrible", "awful", "legal", "sue"}


def should_escalate(message: str, intent: str, confidence: float) -> tuple[bool, str]:
    """Returns (should_escalate, trigger_reason)."""
    if intent == "escalation":
        return True, "escalation_intent"
    if confidence < 0.55:
        return True, "low_confidence"
    words = set(message.lower().split())
    if words & ESCALATION_KEYWORDS:
        return True, "keyword"
    return False, ""


def generate_summary(session_id: str, history: list[dict]) -> str:
    if not history:
        return "No conversation context available."
    formatted = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in history[-10:])
    response = _client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": (
                "Summarize the following airline support conversation in 2-3 sentences, "
                "focusing on what the customer needs and why it could not be resolved:\n\n"
                + formatted
            )
        }],
        max_tokens=150,
    )
    return response.choices[0].message.content
