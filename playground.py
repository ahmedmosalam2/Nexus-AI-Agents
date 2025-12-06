import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.rag_service import RagService

async def main():
    print(" Starting Nexus System Test...\n")

    try:
        rag = RagService()
        print("✅ Service Initialized Successfully.")
    except Exception as e:
        print(f" Error Initializing Service: {e}")
        return
    test_text = "Nexus AI is a special project developed by Eng. Ahmed Mosalam using Clean Architecture principles."
    
    print(f"\n Learning: '{test_text}'")
    try:
        await rag.add_knowledge(test_text)
        print(" Knowledge Added to Vector DB.")
    except Exception as e:
        print(f" Error Adding Knowledge: {e}")
        return
    question = "Who developed the Nexus AI project?"
    print(f"\ Asking: '{question}'")
    
    try:
        answer = await rag.ask(question)
        print("\n" + "="*30)
        print(" AGENT ANSWER:")
        print(answer)
        print("="*30 + "\n")
        
        # تحقق بسيط
        if "Ahmed" in answer:
            print(" TEST PASSED! The agent retrieved the correct name.")
        else:
            print(" TEST WARNING: The answer might be hallucinated or incomplete.")
            
    except Exception as e:
        print(f" Error During Generation: {e}")

if __name__ == "__main__":
    # تشغيل الكود الـ Async
    asyncio.run(main())