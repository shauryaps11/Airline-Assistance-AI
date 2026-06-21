import base64
from openai import OpenAI
from backend.config import settings

_client = OpenAI(api_key=settings.openai_api_key)


def artist(city: str) -> str:
    """Generate a DALL-E 3 destination image and return base64-encoded PNG."""
    prompt = (
        f"A stunning travel poster for {city} showing iconic landmarks, "
        f"local culture and vibrant scenery in a vivid pop-art illustration style."
    )
    response = _client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        response_format="b64_json",
        n=1,
    )
    return response.data[0].b64_json
