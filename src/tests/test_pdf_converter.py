from src.mcp_server.routes.raw_input_tool import generate_resume_from_text
from src.mcp_server.utils import docx_to_pdf

text = """
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

buffer = generate_resume_from_text(text)

print("GOT THE BUFFER")



print("GOT THE PDF BUFFER IN TEST FILE!")
print("PDF Buffer")