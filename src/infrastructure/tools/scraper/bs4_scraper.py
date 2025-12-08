import aiohttp
from bs4 import BeautifulSoup
from src.infrastructure.tools.scraper.base import BaseScraper

class BeautifulSoupScraper(BaseScraper):
    async def scrape(self, url: str) -> str:
        print(f" Scraping URL: {url}...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status != 200:
                        return f"Error: Failed to retrieve content (Status: {response.status})"
                    
                    html_content = await response.text()
                    
                    soup = BeautifulSoup(html_content, 'html.parser')
                    

                    for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                        script.extract()

                    text = soup.get_text(separator='\n')
                
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    

                    return text[:10000] 

        except Exception as e:
            return f"Error scraping website: {str(e)}"