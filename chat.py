import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from image_generator import artist
from audio_generator import talker
from openai.types.chat import ChatCompletionMessageParam

# Load environment variables
load_dotenv()
openai = OpenAI()
MODEL = "gpt-4o"

# System prompt
system_message = (
    "You are a helpful assistant for an airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so."
)

# Tool function (ticket prices)
ticket_prices = {
    "london": "$799",
    "paris": "$899",
    "tokyo": "$1400",
    "berlin": "$499"
}

def get_ticket_price(destination_city):
    print(f"🔧 get_ticket_price called for {destination_city}")
    return ticket_prices.get(destination_city.lower(), "Unknown")

# Tool schema
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to"
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

# Tool handler
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)

    response: ChatCompletionMessageParam = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"The return ticket price to {city.title()} is {price}."
    }

    return response, city

# Main chat function
def chat(message, history):
    try:
        if history is None:
            history = []

        # ✅ Correct format: content is a string
        messages = [{"role": "system", "content": system_message}]

        for item in history:
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })

        messages.append({"role": "user", "content": message})

        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )
        image = None

        # Tool call handling
        if response.choices[0].finish_reason == "tool_calls":
            tool_msg = response.choices[0].message
            tool_response, city = handle_tool_call(tool_msg)
            messages.append(tool_msg)
            messages.append(tool_response)

            # Generate image
            image = artist(city)

            response = openai.chat.completions.create(
                model=MODEL,
                messages=messages
            )

        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})

        # Generate voice
        talker(reply)

        return history, image

    except Exception as e:
        print("🔴 Error in chat():", str(e))
        history = history or []
        history.append({
            "role": "assistant",
            "content": "Something went wrong. Check the terminal for details."
        })
        return history, None
