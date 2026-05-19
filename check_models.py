import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

models = client.models.list()

print("\n✅ AVAILABLE GEMINI MODELS:\n")

for m in models:
    print(m.name)