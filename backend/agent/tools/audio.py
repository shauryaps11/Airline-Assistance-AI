import base64
from io import BytesIO
from openai import OpenAI
from backend.config import settings

_client = OpenAI(api_key=settings.openai_api_key)


def talker(message: str) -> str:
    """Generate TTS audio and return base64-encoded MP3."""
    response = _client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=message,
    )
    buf = BytesIO()
    for chunk in response.iter_bytes(chunk_size=4096):
        buf.write(chunk)
    return base64.b64encode(buf.getvalue()).decode("utf-8")
