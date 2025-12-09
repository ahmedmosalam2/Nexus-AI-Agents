import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.tools.scraper_tool import WebScraperTool
from src.services.context.compression import ContextCompressor

load_dotenv()

async def main():
    print("Nexus Agent Tool Playground")
    print("============================")
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter the website URL: ").strip()

    if not url:
        print("Error: No URL provided.")
        return

    try:
        print("Initializing components...")
        scraper = WebScraperTool()
        compressor = ContextCompressor()

        print(f"Scraping URL: {url}...")
        raw_content = await scraper.run(url)

        if not raw_content:
            print("Failed to retrieve content.")
            return

        print(f"Retrieved {len(raw_content)} chars.")

        print("Compressing Content...")

        query = "Provide a comprehensive summary of the main topics and entities in this text."
        summary = await compressor.compress(raw_content, query)

        print("\nResult Summary:")
        print("=" * 50)
        print(summary)
        print("=" * 50)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())