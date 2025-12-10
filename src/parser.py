import requests
from bs4 import BeautifulSoup

class ArticleParser:
    """Parse articles using newspaper3k or BeautifulSoup fallback"""
    
    def parse(self, url):
        try:
            from newspaper import Article
            article = Article(url)
            article.download()
            article.parse()
            if article.text: return article.text[:10000], "newspaper3k"
        except: pass
        
        try:
            response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(response.content,'html.parser')
            for tag in soup(["script","style","nav","footer","header"]): tag.decompose()
            paragraphs = soup.find_all('p')
            text=' '.join([p.get_text() for p in paragraphs])
            return text[:10000], "beautifulsoup"
        except: pass
        return "", "failed"
