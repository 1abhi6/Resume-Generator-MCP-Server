import os
import yaml
from jinja2 import Template, Environment, meta


class PromptConfig:
    """
    Loads and manages prompt templates from a YAML config file.
    Supports Jinja2 templating for dynamic prompt generation.
    """

    def __init__(self, file_name: str, config_file=None):
        """
        Initialize PromptConfig by loading the YAML file containing prompt templates.

        Args:
            file_name (str): Base name of the prompt config file (without 'prompt.yaml').
            config_file (str, optional): Full path to the config file. If None, constructs path from file_name.
        """
        if config_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(base_dir, f"{file_name}_prompt.yaml")

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, "r", encoding="utf-8") as f:
            self.prompts = yaml.safe_load(f)

    def get_prompt(self, key: str, **kwargs) -> str:
        """
        Render a prompt template by key, substituting variables using Jinja2.

        Args:
            key (str): The prompt key to retrieve.
            **kwargs: Variables to substitute in the template.

        Returns:
            str: Rendered prompt string.
        """
        prompt_entry = self.prompts["PROMPTS"].get(key)
        if prompt_entry is None:
            raise KeyError(f"Prompt '{key}' not found in config")

        raw_prompt = prompt_entry["template"]
        template = Template(raw_prompt)
        return template.render(**kwargs)

    def get_prompt_variables(self, key: str, with_description=False):
        """
        Extract variable names used in a prompt template.

        Args:
            key (str): The prompt key to inspect.
            with_description (bool): If True, return variable descriptions from config.

        Returns:
            set or dict: Set of variable names, or dict of variable names to descriptions.
        """
        prompt_entry = self.prompts["PROMPTS"].get(key)
        if prompt_entry is None:
            raise KeyError(f"Prompt '{key}' not found in config")

        raw_prompt = prompt_entry["template"]

        # Extract variables from template using Jinja2 meta
        env = Environment()
        parsed_content = env.parse(raw_prompt)
        vars_in_template = meta.find_undeclared_variables(parsed_content)

        if with_description:
            descriptions = prompt_entry.get("variables", {})
            return {
                var: descriptions.get(var, "No description provided")
                for var in vars_in_template
            }

        return vars_in_template
