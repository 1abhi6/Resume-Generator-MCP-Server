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
Here’s a story version of **Abhishek Gupta’s** resume — including all details and dummy links where needed:

---

### **The Journey of Abhishek Gupta: From Curious Learner to AI Innovator**

Abhishek Gupta — an ambitious and forward-thinking technologist from Mumbai, India — has always been driven by curiosity and a desire to create meaningful digital solutions. You can explore his professional footprint on [LinkedIn](https://www.linkedin.com/in/abhishekgupta) or dive into his code on [GitHub](https://github.com/abhishekgupta).

#### **The Foundation of Skills**

Abhishek’s expertise spans a rich ecosystem of technologies and methodologies.
He’s proficient in **Programming Languages, AI & LLM Tools** such as Python, LangChain, LangGraph, CrewAI, AutoGen, Agno, RAGs, MCP, LangSmith, RnD, RAG Architecture, and Prompt Engineering.

His **Backend Development** capabilities include frameworks like **FastAPI** and **FastMCP**, while his **Database & ORM** experience covers **PostgreSQL** and **SQLAlchemy**.

In the **Cloud & DevOps** space, Abhishek is skilled with **AWS (Basics)**, **OCI (AI Services)**, **Docker**, **GitHub Actions**, and **CI/CD Pipelines**.

Beyond technical expertise, he possesses a strong set of **Soft Skills** — including communication, client management, team building, and leadership — all of which have fueled his professional growth.

---

#### **Professional Experience**

**Founder and Proprietor – Unarrow Digital Solutions**
📍 *Mumbai, India | Nov 2023 – Aug 2025*

Abhishek founded **Unarrow Digital Solutions**, a digital marketing agency where he combined his technical expertise with entrepreneurial vision.

* He worked with over 20+ businesses, helping them enhance their digital presence.
* His strategies led to clients noticing a **15%–18% improvement in sales** on average.
* He built automation workflows using tools like **Make.com**, **n8n**, and **Zapier** to streamline daily operations.
* Leading a team of 8–10 professionals, he collaborated closely with clients to solve complex business problems using technology-driven approaches.

---

#### **Projects**

**1. BharatLens – Explore Geopolitics Through India’s Perspective**
🔗 [Project Link](https://example.com/bharatlens) | 🔗 [GitHub Link](https://github.com/example/bharatlens)

BharatLens was an innovative platform designed to provide geopolitical insights through an Indian lens.

* Abhishek developed the backend using **FastAPI (JWT auth, chat sessions, message history, OpenAI integration)**.
* The app was deployed on **Render** using **Docker + GitHub Actions CI/CD** for seamless integration.
* He built a secure API layer and integrated **PostgreSQL (Neon)** for persistent storage, enabling RAG-based enhancements and multi-agent architecture for deep analysis.

**2. Expense Tracker MCP Server**
🔗 [Project Link](https://example.com/expensetracker) | 🔗 [GitHub Link](https://github.com/example/expensetracker)

For this project, Abhishek developed a **microservice for tracking expenses** using **FastMCP** integrated with **PostgreSQL** and **SQLAlchemy**.

* He implemented **JWT-based authentication** with role-based access control for user management.
* He built **MCP tools** for managing CRUD operations, budgeting, and automated reporting systems — making the project a strong example of applied backend architecture.

---

#### **Certifications**

Abhishek’s dedication to continuous learning is reflected in his certifications:

* **Oracle Cloud Infrastructure 2025 Certified Generative AI Professional**
  🔗 [View Certificate](https://example.com/oci-genai) – *Sept 2025*
  Focus areas: LangChain, Vector Databases, Semantic Search, and OCI GenAI.

* **Oracle Cloud Infrastructure 2025 Certified AI Foundations Associate**
  🔗 [View Certificate](https://example.com/oci-aifoundations) – *Aug 2025*
  Covered AI/ML fundamentals, OCI AI & ML services, and foundational data engineering concepts.

---

#### **Education**

Abhishek completed his **Bachelor of Science in IT** with **8.1 CGPA** from *Thakur College of Science & Commerce, Kandivali (E), Mumbai* (April 2021 – April 2025).

Prior to that, he completed **HSC** from the same institution in **May 2021** and **SSC** from *St. Joseph English School, Nandhakhal, Virar (W)* with **78.7% in March 2019**.

---

### **Conclusion**

Abhishek Gupta’s journey is a story of relentless learning, innovation, and leadership. From founding his own startup to building advanced RAG-based AI systems, he blends business understanding with technical precision. His ability to automate, optimize, and innovate makes him a promising AI engineer ready to contribute to the next wave of intelligent digital transformation.


"""
prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are a helpful assistant in extracting relevant values from the text as per the provided schema. Parse every information as if you are that person. Always use "I" avoid using "He", "Him", "She", "Her", etc.
            All this data is being processed for resume. So be startegic when choosing text.

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
            
            4. Make sure to complete the sentence within the given word limit.
                Avoid such incomplete sentence:
                Eg 1. Through this course, Abhishek gained hands-on experience designing h
                Eg 2. He explored visual automation design, API integration, and workflow
            """,
        ),
        ("human", text),
    ]
)

model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
structured_model = model.with_structured_output(ResumeSchema)
chain = prompt_template | structured_model

response = chain.invoke({})

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
                    bold=True,
                ),
            }
        )

# --- Process certifications into a list for the template ---
certifications_context = []
certification_section_data = safe_get(
    response, "certification_section", "certifications"
)
if certification_section_data:
    for cert in certification_section_data:
        certifications_context.append(
            {
                "name": cert.name,
                "month": cert.month,
                "year": cert.year,
                "description": cert.description,
                "link": make_link(
                    doc, text="LINK", url=cert.link, underline=True, bold=True
                ),
            }
        )

# --- Process educations into a list for the template ---
educations_context = []
education_section_data = safe_get(response, "education_section", "educations")

if education_section_data:
    for edu in education_section_data:
        educations_context.append(
            {
                "degree": edu.degree,
                "score": edu.score,
                "institution": edu.institution,
                "start_month": edu.start_month,
                "start_year": edu.start_year,
                "end_month": edu.end_month,
                "end_year": edu.end_year,
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
        bold=True,
    ),
    "email_address": make_link(
        doc,
        safe_get(response, "contact_details_section", "email", "text"),
        safe_get(response, "contact_details_section", "email", "link"),
        underline=True,
        bold=True,
    ),
    "linkedin_url": make_link(
        doc,
        "LinkedIn",
        safe_get(response, "contact_details_section", "linkedin_url"),
        underline=True,
        bold=True,
    ),
    "github_url": make_link(
        doc,
        "GitHub",
        safe_get(response, "contact_details_section", "github_url"),
        underline=True,
        bold=True,
    ),
    "skills": safe_get(response, "skills_section", "skills") or [],
    "experiences": safe_get(response, "experience_section", "experiences") or [],
    "projects": projects_context,
    "certifications": certifications_context,
    "educations": educations_context,
}

print(context)

doc.render(context)
doc.save("generated_test.docx")

print("✅ Resume generated successfully!")
