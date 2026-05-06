import os
import json
from dotenv import load_dotenv
from google import genai
import time

from .prompts import flashcards_prompt

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=API_KEY)


def generate_flashcards_with_gemini(text):
    prompt = flashcards_prompt(text)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            raw_text = response.text.strip()
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

            if not raw_text:
                return []

            return json.loads(raw_text)

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed:", e)
            time.sleep(2)

    return []