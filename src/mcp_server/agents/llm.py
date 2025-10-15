import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel

load_dotenv()


class LLM:
    """
    Lightweight wrapper around the ChatOpenAI model used in this project.
    Provides helpers for regular chat responses and structured (pydantic) outputs.
    """

    def __init__(self):
        self.model = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"
        )

    def get__structured_response(
        self,
        resume_pydantic_model: BaseModel,
        prompt_template: ChatPromptTemplate,
    ) -> dict:
        """
        Produce a structured response validated/parsed into the provided pydantic model.

        - resume_pydantic_model: a pydantic BaseModel class describing the expected schema.
        - prompt_template: chat-style prompt to pass to the model.

        Uses model.with_structured_output to enforce structured output and composes the
        prompt_template with the structured model using the chain operator.
        Returns the parsed structured response (typically a dict-like object).
        """

        structured_model = self.model.with_structured_output(resume_pydantic_model)

        chain = prompt_template | structured_model

        response = chain.invoke({})

        return response

    def get_response(self, prompt_template: ChatPromptTemplate) -> str:
        """
        Send a chat-style prompt_template to the model and return the textual content.

        Returns the response.content string from the model invocation.
        """

        chain = prompt_template | self.model

        response = chain.invoke({})

        return response.content
