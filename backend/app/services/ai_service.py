from groq import Groq

from app.core.ai_config import LLM_API_KEY, LLM_MODEL


client = Groq(api_key=LLM_API_KEY)


def ask_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content