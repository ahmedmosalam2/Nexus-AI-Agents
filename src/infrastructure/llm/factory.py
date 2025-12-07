from src.infrastructure.llm.generic_provider import GenericLLMProvider
from src.config.settings import settings

class LLMFactory:
    @staticmethod
    def create_provider():
        provider_type = settings.AI_PROVIDER.lower()
        if provider_type == "gemini":
            print(f"🏭 Factory: Connecting to Google Gemini ({settings.GEMINI_MODEL})...")
            return GenericLLMProvider(

                base_url="https://generativelanguage.googleapis.com/v1beta/openai",
                api_key=settings.GEMINI_API_KEY,
                model=settings.GEMINI_MODEL
            )
        elif provider_type == "ollama":
            print(f"🏭 Factory: Connecting to Local Ollama ({settings.DEFAULT_MODEL})...")
      
            return GenericLLMProvider(
                base_url="http://192.168.1.2:11434/v1", 
                api_key="ollama",
                model=settings.DEFAULT_MODEL
            )
            
        else:
            raise ValueError(f" Unknown AI Provider in .env: {provider_type}")