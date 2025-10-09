from docxtpl import DocxTemplate, RichText
from pydantic_schema.schema1 import ResumeData
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


# Prepare RichText links
def make_link(doc, text: str, url: str):
    if not url:
        return ""
    rt = RichText()
    rt.add(text, url_id=doc.build_url_id(url))
    return rt


model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
structured_model = model.with_structured_output(ResumeData)

human_msg = HumanMessage(
    content="Abhishek Gupta is a 22-year-old male who has recently graduated and is passionate about building intelligent systems. Over the course of his studies, he has worked on several notable projects, including a Resume Generator, an MCP Server, and various RAG (Retrieval-Augmented Generation) Systems. His academic journey and hands-on experience have strengthened his skills in software development and AI engineering, making him a motivated individual eager to contribute to innovative projects. Linkedin is https://www.linkedin.com/in/iautomates, github is https://www.github.com/1abhi6, portfolio wesbite is https://www.abhishekugpta.com "
)

response = structured_model.invoke([human_msg])

links = response.links or {}
doc = DocxTemplate("Document 1.docx")

print(str(response.links.linkedin_url))
make_link_link = make_link(
    doc, "Portfolio Webiste", str(response.links.portfolio_website)
)

print("Make Links: ", make_link_link)

context = {
    "name": response.name,
    "age": response.age,
    "gender": response.gender,
    "qualification": response.qualification,
    "projects": response.projects,
    "linkedin_url": make_link(doc, "LinkedIn", str(response.links.linkedin_url)),
    "github_url": make_link(doc, "Github", str(response.links.github_url)),
    "portfolio_website": make_link(
        doc, "Portfolio Webiste", str(response.links.portfolio_website)
    ),
}


print(context)


doc.render(context)
doc.save("generated_doc.docx")
