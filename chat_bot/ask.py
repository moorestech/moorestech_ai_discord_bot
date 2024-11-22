from util import embedding
from util import query_ai

def ask_ai():
    # query_o1_prompt.txtをロード
    with open("manual/query_o1_prompt.txt", "r", encoding="utf-8") as f:
        usr_prompt = f.read()
    with open("manual/rag_reference.txt", "r", encoding="utf-8") as f:
        rag_reference = f.read()
    with open("manual/force_include_file_name.txt", "r", encoding="utf-8") as f:
        force_include_file_name = f.read().splitlines()

    rag_prompt = embedding.create_rag_prompt(rag_reference + usr_prompt, token_limit=24000,force_include_file_name=force_include_file_name)
    print("[ask_ai] rag_prompt:", rag_prompt)

    prompt = rag_prompt + "\n" + usr_prompt

    print("[ask_ai] start query_ai...")
    result = query_ai.query_ai(prompt, query_ai.ModelType.GPT4)
    print("[ask_ai] result:", result)

    return result



