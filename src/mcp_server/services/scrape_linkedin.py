import os
import requests
from dotenv import load_dotenv
from src.mcp_server.utils import get_username

# Load environment variables from .env file
load_dotenv()

class ScrapeLinkedIn:
    """Class to handle LinkedIn profile scraping using ScrapingDog API"""
    
    def __init__(self):
        # Initialize with API key from environment variables
        self.api_key = os.getenv("SCRAPINGDOG_API_KEY")
        self.url = "https://api.scrapingdog.com/profile"

    def scrape(self, linkedin_url: str):
        """
        Scrape LinkedIn profile data using ScrapingDog API
        Args:
            linkedin_url (str): Full LinkedIn profile URL
        Returns:
            str: Raw response text from the API
        Raises:
            ValueError: If URL doesn't contain a valid username
        """
        # Extract username from LinkedIn URL
        linkedin_username = get_username(url=linkedin_url)

        if linkedin_username is None:
            raise ValueError("The provided link don't have a username", linkedin_url)

        # Set up initial API request parameters
        params = {
            "api_key": self.api_key,
            "type": "profile",
            "id": linkedin_username,
            "premium": "false",
        }
        try:
            # Attempt first API request with non-premium parameter
            response = requests.get(self.url, params=params)
        except Exception as e:
            # If first attempt fails, retry with premium parameter
            print(f"{e} \nNow trying again with premium=true parameter")
            params = {
                "api_key": self.api_key,
                "type": "profile",
                "id": linkedin_username,
                "premium": "true",
            }
            response = requests.get(self.url, params=params)

        # Check if request was successful
        if response.status_code == 200:
            return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
