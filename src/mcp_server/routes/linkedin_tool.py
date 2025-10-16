# Tool for Linkedin URL input

from dotenv import load_dotenv

from src.mcp_server.agents import LightLLM
from src.mcp_server.prompts import PromptConfig
from src.mcp_server.routes.common_logic import get_common_logic
from src.mcp_server.services import ScrapeLinkedIn


def linkedin(linkedin_url: str, template_selected: str) -> dict:
    """
    Process a LinkedIn profile URL and return a structured response for resume generation.

    Args:
        linkedin_url (str): Public LinkedIn profile URL to scrape.
        template_selected (str): Selected resume/template identifier.

    Returns:
        dict: Result produced by get_common_logic (structured resume/response).
    """
    load_dotenv()

    # Scrape LinkedIn
    scrape_linkedin_obj = ScrapeLinkedIn()
    linkedin_response = scrape_linkedin_obj.scrape(linkedin_url=linkedin_url)

    # Organise LinkedIn Data
    prompt_config = PromptConfig(file_name="linkedin_data")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    light_llm_obj = LightLLM()
    user_persona = light_llm_obj.get_response(
        system_prompt=system_prompt, user_prompt=linkedin_response
    )

    # Send to common logic
    response = get_common_logic(
        enhanced_persona=user_persona, template_selected=template_selected
    )

    return response

