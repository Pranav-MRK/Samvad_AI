from google import genai

from app.core.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"


def classify_intent(user_input: str) -> str:
    prompt = f"""
You are the intent classifier for an enterprise voice AI agent.

Classify the user's request into exactly ONE of these intents:

- admission_documents
- application_status
- fee_information
- technical_support
- appointment
- general_query

User request:
{user_input}

Return only the intent name.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    if response.text is None:
        raise RuntimeError("Gemini returned an empty response")

    return response.text.strip()