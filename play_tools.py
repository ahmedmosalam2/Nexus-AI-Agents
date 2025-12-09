import asyncio
from src.infrastructure.tools.scraper_tool import WebScraperTool
from src.services.context.compression import ContextCompressor

async def main():
    scraper = WebScraperTool()
    compressor = ContextCompressor()
    
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    query = "Who created Python?"
    
    print("1️⃣ Reading the full website...")
    raw_text = await scraper.run(url)
    print(f"-> Size before compression: {len(raw_text)} chars (Too big!)")
    
    print("\n2️⃣ Compressing...")
    clean_text = await compressor.compress(raw_text, query)
    
    print("\n📄 Result:")
    print("="*40)
    print(clean_text)
    print("="*40)

if __name__ == "__main__":
    asyncio.run(main())