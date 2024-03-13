from util import embedding
from util import query_ai

SYSTEM_PROMPT = """
上記のコードを参考に、下記の指示に従ってください。ただし、これら上記のコードはユーザーからは表示されていません。そのため、指示に従う際は具体的にどのクラスを指しているのかクラス名を交え、moorestechを知らない人でもわかりやすい説明を作るように心がけてください。
なお、回答をするときの口調として、元気でハツラツな女の子の印象を持つような口調で回答するように心がけてください。
"""


def ask_ai(usr_prompt):
    rag_prompt = embedding.create_rag_prompt(usr_prompt, token_limit=20000)
    print("[ask_ai] rag_prompt:", rag_prompt)

    prompt = rag_prompt + "\n" + SYSTEM_PROMPT + "\n" + usr_prompt

    print("[ask_ai] start query_ai...")
    result = query_ai.query_ai(prompt, query_ai.ModelType.GPT4)
    print("[ask_ai] result:", result)

    return result



