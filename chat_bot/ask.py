from util import embedding
from util import query_ai

async def ask_ai_stream(usr_prompt):
    with open("manual/rag_reference.txt", "r", encoding="utf-8") as f:
        rag_reference = f.read()
    with open("manual/force_include_file_name.txt", "r", encoding="utf-8") as f:
        force_include_file_name = f.read().splitlines()

    rag_prompt = embedding.create_rag_prompt(
        rag_reference + usr_prompt,
        token_limit=5,
        force_include_file_name=force_include_file_name
    )

    prompt = rag_prompt + "\n" + usr_prompt

    print("[ask_ai_stream] start query_ai_stream...")
    async for chunk in query_ai.query_ai_stream_gpt4(prompt):
        yield chunk
