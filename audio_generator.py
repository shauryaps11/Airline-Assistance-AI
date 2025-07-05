from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def talker(message):
    try:
        speech_file_path = "response.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=message
        )
        response.stream_to_file(speech_file_path)
        os.system(f"afplay {speech_file_path}")  # macOS only
    except Exception as e:
        print("🔴 Error in talker():", str(e))
