from src.mcp_server.prompts import PromptConfig
from langchain_core.prompts import ChatPromptTemplate
from src.mcp_server.agents import LLM

prompt_config = PromptConfig(file_name="jd_ehnancer")
system_prompt = prompt_config.get_prompt(key="system_prompt")

print(system_prompt)

jd = """
Python + Gen AI

Job Summary

We are seeking a skilled Developer with 5 to 8 years of experience to join our team in a hybrid work model. The ideal candidate will have expertise in Semantic Search Agentic AI and Generative AI. This role involves developing innovative solutions that leverage AI technologies to enhance our products and services. The position offers an opportunity to work in a dynamic environment with a focus on cutting-edge AI applications.

Responsibilities

Develop and implement AI-driven solutions using Semantic Search Agentic AI and Generative AI to improve product functionality and user experience.
Collaborate with cross-functional teams to design and deploy AI models that meet business requirements and enhance operational efficiency.
Conduct thorough testing and validation of AI models to ensure accuracy reliability and performance in real-world scenarios.
Optimize AI algorithms for scalability and integration with existing systems to support seamless deployment and maintenance.
Provide technical expertise and guidance to team members on best practices in AI development and implementation.
Stay updated with the latest advancements in AI technologies and incorporate relevant innovations into ongoing projects.
Analyze and interpret complex data sets to derive actionable insights and drive data-informed decision-making processes.
Document AI development processes methodologies and outcomes to facilitate knowledge sharing and continuous improvement.
Engage in code reviews and provide constructive feedback to peers to maintain high-quality code standards.
Troubleshoot and resolve technical issues related to AI applications to ensure smooth and uninterrupted operation.
Participate in project planning and contribute to the development of project timelines and deliverables.
Communicate effectively with stakeholders to understand project goals and align AI solutions with organizational objectives.
Ensure compliance with data privacy and security regulations in all AI-related activities.
Qualifications

Possess a strong understanding of Semantic Search Agentic AI and Generative AI technologies.
Demonstrate proficiency in programming languages commonly used in AI development such as Python or Java.
Exhibit excellent problem-solving skills and the ability to work independently and collaboratively in a team environment.
Show a track record of successful AI project implementations and the ability to manage multiple projects simultaneously.
Have a keen interest in staying abreast of emerging AI trends and technologies.
Display strong communication skills to effectively convey technical concepts to non-technical stakeholders.
Hold a bachelors degree in computer science engineering or a related field.
Role: Software Development - Other
Industry Type: IT Services & Consulting
Department: Engineering - Software & QA
Employment Type: Full Time, Permanent
Role Category: Software Development
Education
UG: Any Graduate
Key Skills
Skills highlighted with ‘‘ are preferred keyskills
Gen AI Developer
Gen AIPython API
"""


prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", jd),
        ]
    )

llm_obj = LLM()
enhanced_jd = llm_obj.get_response(prompt_template=prompt_template)

print(enhanced_jd)