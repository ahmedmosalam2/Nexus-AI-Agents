from src.infrastructure.llm.factory import LLMFactory

class ContextCompressor:
    def __init__(self):
    
        self.llm = LLMFactory.create_provider()

    async def compress(self, text: str, query: str) -> str:
        """
        الوظيفة: تاخد نص طويل جداً، وترجع ملخص مفيد ليه علاقة بالسؤال.
        """
      
        if len(text) < 1000:
            return text

        print(f"🗜️ Compressing content... (Raw length: {len(text)})")

  
        prompt = f"""
        You are a helpful research assistant.
        I have scraped a long website content regarding this query: "{query}".
        
        Please extract ONLY the relevant information that answers the query.
        - Remove ads, navigation menus, and unrelated text.
        - Summarize the key points.
        - If the text is not relevant, say "No relevant info".

        --- Raw Content ---
        {text[:15000]} 
        -------------------
        
        Relevant Summary:
        """

        try:
      
            summary = await self.llm.generate_text(
                prompt=prompt,
                max_output_tokens=500, 
                temperature=0.2
            )
            return summary
        except Exception as e:
            print(f" Compression Failed: {e}")
            return text[:2000] 