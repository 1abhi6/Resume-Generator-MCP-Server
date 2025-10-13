# The test is passed and working!

from src.mcp_server.prompts import PromptConfig

prompt_config = PromptConfig(file_name="central_llm")

prompt = prompt_config.get_prompt(key="system_prompt")

# print(prompt)


# variables = prompt_config.get_prompt_variables(key="system_prompt", with_description=True)
# print("\n\nHere is the variable: ", variables)