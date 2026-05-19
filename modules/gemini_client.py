import os
from google import genai

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, model="gemini-1.5-flash"):
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text if response and response.text else None

        except Exception as e:
            print("Gemini Error:", e)
            return None


# global instance
gemini = GeminiClient()