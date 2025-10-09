from docxtpl import DocxTemplate
from typing import List
from pydantic import BaseModel
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()


# Pydantic Schema
class Person(BaseModel):
    name: str
    age: int
    gender: str
    qualification: str
    projects: List[str]


model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
structured_model = model.with_structured_output(Person)

human_msg = HumanMessage(
    content="Abhishek Gupta is a 22-year-old male who has recently graduated and is passionate about building intelligent systems. Over the course of his studies, he has worked on several notable projects, including a Resume Generator, an MCP Server, and various RAG (Retrieval-Augmented Generation) Systems. His academic journey and hands-on experience have strengthened his skills in software development and AI engineering, making him a motivated individual eager to contribute to innovative projects."
)

context = structured_model.invoke([human_msg])


print(context)

doc = DocxTemplate("demo1.docx")
doc.render(context)
doc.save("generated_doc.docx")
