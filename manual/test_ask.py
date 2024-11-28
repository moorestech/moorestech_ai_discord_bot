import asyncio
from chat_bot import ask
from util import embedding

async def run_ask_ai_stream(prompt):
    results = []
    async for chunk in ask.ask_ai_stream(prompt):
        results.append(chunk)
    return results

if __name__ == "__main__":
    embedding.update_embedding()
    result = asyncio.run(run_ask_ai_stream("コードについて教えて下さい。"))
    print(f"Result: {result}")
