import asyncio

from src.infrastructure.tools.search_tool import WebSearchTool

async def main():
    print(" Testing Enterprise Search Tool (DuckDuckGo)...\n")
    
   
    search_tool = WebSearchTool(max_results=3)

    query = "who is Messi?"
    
    print(f" Asking: {query}")
    try:
        result = await search_tool.run(query)
        print("\n📄 Agent Report:")
        print("="*40)
        print(result)
        print("="*40)
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())