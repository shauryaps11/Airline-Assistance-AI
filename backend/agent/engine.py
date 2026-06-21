import json
from openai import OpenAI
from backend.config import settings
from backend.models import ChatResponse
from backend.agent import intent as intent_mod
from backend.agent import memory as memory_mod
from backend.agent import escalation as escalation_mod
from backend.agent.tools.pricing import get_ticket_price, PRICE_TOOL_SCHEMA
from backend.agent.tools.image import artist
from backend.agent.tools.audio import talker
from backend import database as db

_client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = (
    "You are SkyAssist, a friendly and knowledgeable airline customer support agent. "
    "Give helpful, accurate, concise answers. "
    "If asked about ticket prices, always quote the exact price returned by the tool. "
    "If you don't know something, say so honestly."
)


def process(session_id: str, message: str) -> ChatResponse:
    db.upsert_session(session_id)

    # Step 1: retrieve relevant memory
    snippets = memory_mod.retrieve(session_id, message)

    # Step 2: classify intent
    classification = intent_mod.classify(message, snippets)
    intent = classification.get("intent", "general_faq")
    confidence = float(classification.get("confidence", 0.5))
    params = classification.get("params", {})
    city = params.get("destination_city") if params else None

    # Step 3: check escalation
    do_escalate, escalation_trigger = escalation_mod.should_escalate(message, intent, confidence)
    escalation_summary = None

    # Step 4: build messages for GPT-4o
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if snippets:
        context_block = "Relevant context from this conversation:\n" + "\n---\n".join(snippets)
        messages.append({"role": "system", "content": context_block})
    messages.append({"role": "user", "content": message})

    tools_used = []
    image_b64 = None
    audio_b64 = None

    if do_escalate:
        history = db.get_session_messages(session_id)
        escalation_summary = escalation_mod.generate_summary(session_id, history)
        db.log_escalation(session_id, escalation_trigger, escalation_summary)
        reply = (
            "I'm sorry you're experiencing this issue. I've flagged your conversation "
            "for a human agent who will follow up shortly. Please hold on."
        )
    else:
        # Step 5: tool dispatch based on intent
        if intent in ("price_inquiry", "destination_image") and city:
            response = _client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[PRICE_TOOL_SCHEMA],
                tool_choice="auto",
            )
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":
                tool_call = choice.message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                queried_city = args.get("destination_city", city)
                price = get_ticket_price(queried_city)
                tools_used.append("get_ticket_price")

                tool_result_msg = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Return ticket to {queried_city.title()}: {price}",
                }
                messages.append(choice.message)
                messages.append(tool_result_msg)

                # Generate destination image for destination_image intent
                if intent == "destination_image":
                    try:
                        image_b64 = artist(queried_city)
                        tools_used.append("dall-e-3")
                    except Exception:
                        pass

                final_response = _client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                )
                reply = final_response.choices[0].message.content
            else:
                reply = choice.message.content
        else:
            response = _client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            reply = response.choices[0].message.content

        # Step 6: generate audio
        try:
            audio_b64 = talker(reply)
            tools_used.append("tts-1")
        except Exception:
            pass

    # Step 7: persist to memory + SQLite
    memory_mod.store(session_id, message, reply, intent)
    db.log_message(session_id, "user", message)
    db.log_message(
        session_id, "assistant", reply,
        intent=intent, confidence=confidence,
        tools_used=tools_used, escalated=do_escalate
    )

    return ChatResponse(
        reply=reply,
        intent=intent,
        confidence=confidence,
        tools_used=tools_used,
        escalated=do_escalate,
        escalation_summary=escalation_summary,
        image_b64=image_b64,
        audio_b64=audio_b64,
    )
