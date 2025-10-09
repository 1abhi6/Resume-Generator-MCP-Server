from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAI_LLM:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.api_key)

    def get_model(self):
        return self.model
