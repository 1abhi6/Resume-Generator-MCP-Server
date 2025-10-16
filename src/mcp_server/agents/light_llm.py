import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LightLLM:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._model = model

    def get_response(self, system_prompt: str, user_prompt: str):
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(user_prompt)},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()
