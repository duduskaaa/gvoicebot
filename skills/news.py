import os

import requests

from skills.base import Skill

_BASE_URL = "https://newsapi.org/v2/top-headlines"


class NewsSkill(Skill):
    keywords = ["news", "headlines", "what's happening"]

    def execute(self, text: str) -> str:
        api_key = os.environ.get("NEWS_API")
        if not api_key:
            return "NewsAPI key is not set. Please set the NEWS_API environment variable."
        try:
            response = requests.get(
                _BASE_URL,
                params={"language": "en", "pageSize": 5, "apiKey": api_key},
                timeout=5,
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])
            if not articles:
                return "No news available at the moment."
            headlines = [f"{i + 1}. {a['title']}" for i, a in enumerate(articles)]
            return "Top news:\n" + "\n".join(headlines)
        except requests.exceptions.Timeout:
            return "Could not retrieve news: request timed out."
        except requests.exceptions.RequestException:
            return "Could not retrieve news. Check your internet connection."
