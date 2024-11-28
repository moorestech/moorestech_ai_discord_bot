import discord
from discord import WebhookMessage

from util import embedding
from util import query_ai


async def ask_ai_stream(usr_prompt):
    with open("manual/rag_reference.txt", "r", encoding="utf-8") as f:
        rag_reference = f.read()
    with open("manual/force_include_file_name.txt", "r", encoding="utf-8") as f:
        force_include_file_name = f.read().splitlines()

    rag_prompt = embedding.create_rag_prompt(
        rag_reference + usr_prompt,
        token_limit=10000,
        force_include_file_name=force_include_file_name
    )

    prompt = rag_prompt + "\n" + usr_prompt

    print("[ask_ai_stream] start query_ai_stream...")
    async for chunk in query_ai.query_ai_stream_gpt4(prompt):
        yield chunk


async def run_ask_ai_stream(response_message: WebhookMessage, question: str):
    collected_response = ""
    async for chunk in ask_ai_stream(question):
        collected_response += chunk
        # 2000字に収まるように調整
        display_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + collected_response[:2000]
        await response_message.edit(content=display_response)