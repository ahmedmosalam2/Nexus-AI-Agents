import aiohttp
import ssl
import random
from bs4 import BeautifulSoup
from src.infrastructure.tools.scraper.base import BaseScraper

class BeautifulSoupScraper(BaseScraper):
    async def scrape(self, url: str) -> str:
        print(f" Scraping URL: {url}...")
 
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        try:
            async with aiohttp.ClientSession() as session:
          
                async with session.get(url, headers=headers, ssl=ssl_context, timeout=15) as response:
                    
                    if response.status != 200:
                      
                        error_msg = f"Error: HTTP Status {response.status}"
                        try:
                           
                            fail_text = await response.text()
                            if "CAPTCHA" in fail_text:
                                error_msg += " (Blocked by CAPTCHA)"
                        except:
                            pass
                        return error_msg
                    
                 
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
               
                    for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "noscript"]):
                        element.extract()

                    text = soup.get_text(separator='\n')
                 
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
   
                    return text[:15000]

        except Exception as e:
            return f"Error details: {str(e)}"