TICKET_PRICES = {
    "london": "$799",
    "paris": "$899",
    "tokyo": "$1400",
    "berlin": "$499",
    "new york": "$299",
    "dubai": "$950",
    "sydney": "$1600",
    "rome": "$749",
    "barcelona": "$699",
    "singapore": "$1250",
}

PRICE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_ticket_price",
        "description": "Get the price of a return ticket to the destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city the customer wants to fly to"
                }
            },
            "required": ["destination_city"],
            "additionalProperties": False
        }
    }
}


def get_ticket_price(destination_city: str) -> str:
    return TICKET_PRICES.get(destination_city.lower().strip(), "Unknown — we may not fly there yet")
