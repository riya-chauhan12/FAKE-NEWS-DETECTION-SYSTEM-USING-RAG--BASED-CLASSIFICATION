import requests
from typing import List, Dict

class MultiSourceSearcher:
    """Search multiple APIs with fallback"""

    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys or {}

        # Reliability scores
        self.source_reliability = {
            "reuters": 0.95, "associated press": 0.95, "ap news": 0.95,
            "bbc": 0.90, "npr": 0.90, "pbs": 0.90,
            "cnn": 0.75, "fox news": 0.75, "msnbc": 0.75,
            "default": 0.60
        }

    def search(self, claim: str, max_results: int = 10) -> List[Dict]:
        """Search news from available APIs"""

        results = []

        # GNews
        if "gnews" in self.api_keys:
            results.extend(self._search_gnews(claim, max_results))

        # NewsAPI
        if "newsapi" in self.api_keys:
            results.extend(self._search_newsapi(claim, max_results))

        # Bing
        if "bing" in self.api_keys:
            results.extend(self._search_bing(claim, max_results))

        # Deduplicate & reliability score
        results = self._deduplicate(results)
        results = self._add_reliability(results)

        return results[:max_results]

    # ----------------- GNEWS --------------------
    def _search_gnews(self, query: str, limit: int) -> List[Dict]:
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": query,
                "token": self.api_keys["gnews"],
                "lang": "en",
                "max": limit,
                "sortby": "relevance"
            }

            res = requests.get(url, params=params, timeout=10)
            data = res.json().get("articles", [])

            return [{
                "title": a["title"],
                "url": a["url"],
                "source": a["source"]["name"],
                "published": a.get("publishedAt", ""),
                "description": a.get("description", ""),
                "content": a.get("content", "")
            } for a in data]

        except:
            return []

    # ----------------- NEWSAPI --------------------
    def _search_newsapi(self, query: str, limit: int) -> List[Dict]:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": self.api_keys["newsapi"],
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": limit,
            }

            res = requests.get(url, params=params, timeout=10)
            data = res.json().get("articles", [])

            return [{
                "title": a["title"],
                "url": a["url"],
                "source": a["source"]["name"],
                "published": a.get("publishedAt", ""),
                "description": a.get("description", ""),
                "content": a.get("content", "")
            } for a in data]

        except:
            return []

    # ----------------- BING NEWS --------------------
    def _search_bing(self, query: str, limit: int) -> List[Dict]:
        try:
            url = "https://api.bing.microsoft.com/v7.0/news/search"
            headers = {"Ocp-Apim-Subscription-Key": self.api_keys["bing"]}
            params = {"q": query, "count": limit, "mkt": "en-US"}

            res = requests.get(url, headers=headers, params=params, timeout=10)
            data = res.json().get("value", [])

            return [{
                "title": a["name"],
                "url": a["url"],
                "source": a.get("provider", [{}])[0].get("name", "Unknown"),
                "published": a.get("datePublished", ""),
                "description": a.get("description", ""),
                "content": "",
            } for a in data]

        except:
            return []

    # ----------------- HELPERS --------------------
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []

        for r in results:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique.append(r)

        return unique

    def _add_reliability(self, results: List[Dict]) -> List[Dict]:
        for r in results:
            src = r["source"].lower()
            r["reliability"] = self.source_reliability.get(src, 0.60)

        return results
