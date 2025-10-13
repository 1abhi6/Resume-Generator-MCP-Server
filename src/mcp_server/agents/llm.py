from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
import os

load_dotenv()


class LLM:
    def __init__(self):
        self.model = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"
        )

    def get_response(
        self, resume_pydantic_model: BaseModel, prompt_template: ChatPromptTemplate
    ):
        structured_model = self.model.with_structured_output(resume_pydantic_model)
        chain = prompt_template | structured_model

        response = chain.invoke({})

        return response
