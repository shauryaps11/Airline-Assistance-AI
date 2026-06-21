import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import get_ticket_price, price_function
from image_generator import artist
from audio_response import talker

load_dotenv()
openai = OpenAI()
MODEL = "gpt-4o-mini"

system_message = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers. Be accurate. Say 'I don't know' if unsure."
)

tools = [{"type": "function", "function": price_function}]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

def chat(message, history):
    try:
        messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        image = None

        if response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            response, city = handle_tool_call(message)
            messages.append(message)
            messages.append(response)
            image = artist(city)  # <-- Possible failure point
            response = openai.chat.completions.create(model=MODEL, messages=messages)

        reply = response.choices[0].message.content
        history += [{"role": "assistant", "content": reply}]

        # Comment this temporarily if unsure:
        talker(reply)  # <-- Possible failure point

        return history, image

    except Exception as e:
        print("🔴 ERROR in chat():", str(e))
        return history + [{"role": "assistant", "content": "An error occurred. Please try again."}], None
