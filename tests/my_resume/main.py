from pydantic_schema import ResumeSchema
from docxtpl import DocxTemplate, RichText
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


def make_link(doc, text: str | None, url: str | None, underline=False, bold=False):
    """Create a RichText hyperlink safely with optional underline and bold."""
    if not text or not url:
        return ""
    rt = RichText()
    rt.add(text, url_id=doc.build_url_id(url), underline=underline, bold=bold)
    return rt


def safe_get(obj, *attrs):
    """Safely navigate nested dicts or objects."""
    for attr in attrs:
        if obj is None:
            return None
        if isinstance(obj, dict):
            obj = obj.get(attr)
        else:
            obj = getattr(obj, attr, None)
    return obj


doc = DocxTemplate("test2.docx")

text = """
Abhishek Gupta
Phone: +919876543210
Email: [abhishek@email.com](mailto:abhishek@email.com)
LinkedIn: [https://www.linkedin.com/in/abhishek](https://www.linkedin.com/in/abhishek)
GitHub: [https://github.com/abhishek](https://github.com/abhishek)

Abhishek is a passionate technologist and entrepreneur based in Mumbai, India, with strong expertise in AI, automation, and full-stack development. He founded Unarrow Digital Solutions and grew it to serve over twenty clients, delivering marketing campaigns that improved client sales by an average of 15–18%. He built automation workflows with Make.com, n8n, and Zapier to save clients hours of manual work each week, and led a team of 8–10 professionals to translate business problems into scalable technical solutions.

In parallel with his entrepreneurial work, Abhishek moved into AI automation as a freelance engineer. Since September 2025 he has been building intelligent chatbots and workflow automations using FastAPI, LangChain, and OpenAI’s GPT models. His freelance work focuses on integrating AI into real business processes, designing RAG-based agents and prompt-engineered solutions, and building monitoring dashboards with Streamlit.

Skills:

* Programming: Python, FastAPI, LangChain, React.js
* AI & ML: OpenAI API, Vector Databases, RAG Pipelines
* Automation: n8n, Zapier, Make.com
* Tools & Cloud: Docker, Vercel, Render, GitHub Actions

Professional Experience:

* Founder and Proprietor, Unarrow Digital Solutions — Mumbai, India (Nov 2023 - Aug 2025)

  * Founded and managed a digital marketing agency serving 20+ clients across India.
  * Delivered campaigns that improved average client sales by 15–18%.
  * Built automation workflows using Make.com, n8n, and Zapier to streamline client operations.
  * Led a team of 8–10 professionals and collaborated with clients to solve complex business problems.

* AI Automation Engineer (Freelance), Freelance Projects — Remote, India (Sep 2025 - Present)

  * Developed AI chatbots using FastAPI and LangChain for customer support automation.
  * Integrated OpenAI GPT models with business workflows for marketing automation.
  * Implemented prompt engineering best practices for contextual RAG-based agents.
  * Built dashboards to monitor automation metrics using Streamlit.

Projects:

BharatLens – Explore Geopolitics Through India’s Perspective | LINK: [https://bharatlens.in](https://bharatlens.in)

* Developed backend using FastAPI with JWT authentication, chat sessions, and OpenAI integration.
* Designed frontend in React.js, deployed on Vercel with secure API communication.
* Implemented PostgreSQL (Neon) for persistent data storage and RAG-based knowledge retrieval.
* Deployed on Render using Docker and GitHub Actions for CI/CD pipelines.

Expense Tracker MCP Server | LINK: [https://github.com/abhishek/expense-tracker](https://github.com/abhishek/expense-tracker)

* Built a secure FastMCP-based expense tracking server using PostgreSQL and SQLAlchemy.
* Implemented JWT-based authentication with role-based user access control.
* Developed tools for CRUD operations, budgeting, and automated report generation.
* Containerized application using Docker and deployed on Render cloud platform.

Resume Generator MCP Server | LINK: [https://github.com/abhishek/resume-generator](https://github.com/abhishek/resume-generator)

* Created an AI-powered resume generator using LangChain and OpenAI API.
* Implemented dynamic Jinja2 templates to generate .docx resumes automatically.
* Built modular Pydantic schemas for structured resume data validation.
* Added support for project-based sections with bullet formatting and hyperlinks.

Abhishek combines a practical product mindset with hands-on engineering skills. He thrives on building end-to-end systems—backends, frontends, and AI layers—that solve real problems and scale reliably. If you’d like to connect or see demos of his work, reach out via the contact details above.

"""

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are a helpful assistant in extracting relevant values from the text as per the provided schema.
            ## When extracting the values make sure to adhere the following guidelines.
            1. If the phone number link is separated with dash or spaces then remove all the dashes or spaces.
                - Eg 1. tel:+1-555-1234 -> tel:+15551234
                - Eg 2. tel:+1 555 1234 -> tel:+15551234

            2. All the links should have valid structure. Start with https://www or http://www
                If there is any link without this structure, append https://www or http://www yourself.
                - Eg 1. abhishekgupta.com -> https://www.abhishekgupta.com

            3. If user has only provided the username for any platform, then try to convert it into proper link.
                - Eg 1. LinkedIn: iautomates -> https://www.linkedin.com/in/iautomates
                - Eg 2. Github: 1abhi6 -> https://www.github.com/1abhi6
            """,
        ),
        ("human", text),
    ]
)

model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
structured_model = model.with_structured_output(ResumeSchema)
chain = prompt_template | structured_model

response = chain.invoke({})

# response = {
#     "name_section": {"candidate_name": "Abhishek Gupta"},
#     "contact_details_section": {
#         "phone": {"text": "+919876543210", "link": "tel:+919876543210"},
#         "email": {"text": "abhishek@email.com", "link": "mailto:abhishek@email.com"},
#         "linkedin_url": "https://www.linkedin.com/in/abhishek",
#         "github_url": "https://github.com/abhishek",
#     },
#     "skills_section": {
#         "skills": [
#             {
#                 "category": "Programming",
#                 "items": ["Python", "FastAPI", "LangChain", "React.js"],
#             },
#             {
#                 "category": "AI & ML",
#                 "items": ["OpenAI API", "Vector Databases", "RAG Pipelines"],
#             },
#             {"category": "Automation", "items": ["n8n", "Zapier", "Make.com"]},
#             {
#                 "category": "Tools & Cloud",
#                 "items": ["Docker", "Vercel", "Render", "GitHub Actions"],
#             },
#         ]
#     },
#     "experience_section": {
#         "experiences": [
#             {
#                 "job_role": "Founder and Proprietor",
#                 "company_name": "Unarrow Digital Solutions",
#                 "city": "Mumbai",
#                 "country": "India",
#                 "start_month": "Nov",
#                 "start_year": "2023",
#                 "end_month": "Aug",
#                 "end_year": "2025",
#                 "points": [
#                     "Founded and managed a digital marketing agency serving 20+ clients across India.",
#                     "Delivered campaigns that improved average client sales by 15–18%.",
#                     "Built automation workflows using Make.com, n8n, and Zapier to streamline client operations.",
#                     "Led a team of 8–10 professionals and collaborated with clients to solve complex business problems.",
#                 ],
#             },
#             {
#                 "job_role": "AI Automation Engineer (Freelance)",
#                 "company_name": "Freelance Projects",
#                 "city": "Remote",
#                 "country": "India",
#                 "start_month": "Sep",
#                 "start_year": "2025",
#                 "end_month": "Present",
#                 "end_year": "",
#                 "points": [
#                     "Developed AI chatbots using FastAPI and LangChain for customer support automation.",
#                     "Integrated OpenAI GPT models with business workflows for marketing automation.",
#                     "Implemented prompt engineering best practices for contextual RAG-based agents.",
#                     "Built dashboards to monitor automation metrics using Streamlit.",
#                 ],
#             },
#         ]
#     },
#     "project_section": {
#         "projects": [
#             {
#                 "project_name": "BharatLens – Explore Geopolitics Through India’s Perspective",
#                 "project_link": "https://bharatlens.in",
#                 "points": [
#                     "Developed backend using FastAPI with JWT authentication, chat sessions, and OpenAI integration.",
#                     "Designed frontend in React.js, deployed on Vercel with secure API communication.",
#                     "Implemented PostgreSQL (Neon) for persistent data storage and RAG-based knowledge retrieval.",
#                     "Deployed on Render using Docker and GitHub Actions for CI/CD pipelines.",
#                 ],
#             },
#             {
#                 "project_name": "Expense Tracker MCP Server",
#                 "project_link": "https://github.com/abhishek/expense-tracker",
#                 "points": [
#                     "Built a secure FastMCP-based expense tracking server using PostgreSQL and SQLAlchemy.",
#                     "Implemented JWT-based authentication with role-based user access control.",
#                     "Developed tools for CRUD operations, budgeting, and automated report generation.",
#                     "Containerized application using Docker and deployed on Render cloud platform.",
#                 ],
#             },
#             {
#                 "project_name": "Resume Generator MCP Server",
#                 "project_link": "https://github.com/abhishek/resume-generator",
#                 "points": [
#                     "Created an AI-powered resume generator using LangChain and OpenAI API.",
#                     "Implemented dynamic Jinja2 templates to generate .docx resumes automatically.",
#                     "Built modular Pydantic schemas for structured resume data validation.",
#                     "Added support for project-based sections with bullet formatting and hyperlinks.",
#                 ],
#             },
#         ]
#     },
# }


# --- Process projects into a list for the template ---
projects_context = []
project_section_data = safe_get(response, "project_section", "projects")

if project_section_data:
    for project in project_section_data:
        # Create a dictionary for each project
        projects_context.append(
            {
                "project_name": project.project_name,
                "points": project.points,
                "project_link": make_link(
                    doc,
                    text="LINK",
                    url=project.project_link,
                    underline=True,
                    bold=True
                ),
            }
        )

# --- Safely extract all values into the final context ---
context = {
    "candidate_name": safe_get(response, "name_section", "candidate_name"),
    "phone_number": make_link(
        doc,
        safe_get(response, "contact_details_section", "phone", "text"),
        safe_get(response, "contact_details_section", "phone", "link"),
        underline=True,
        bold=True
    ),
    "email_address": make_link(
        doc,
        safe_get(response, "contact_details_section", "email", "text"),
        safe_get(response, "contact_details_section", "email", "link"),
        underline=True,
        bold=True
    ),
    "linkedin_url": make_link(
        doc,
        "LinkedIn",
        safe_get(response, "contact_details_section", "linkedin_url"),
        underline=True,
        bold=True
    ),
    "github_url": make_link(
        doc,
        "GitHub",
        safe_get(response, "contact_details_section", "github_url"),
        underline=True,
        bold=True
    ),
    "skills": safe_get(response, "skills_section", "skills") or [],
    "experiences": safe_get(response, "experience_section", "experiences") or [],
    "projects": projects_context,
}

print(context)

doc.render(context)
doc.save("generated_test.docx")

print("✅ Resume generated successfully!")
