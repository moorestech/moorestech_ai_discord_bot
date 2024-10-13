from chat_bot import ask
from mooresmaster import master_rag_prompt
from util import embedding

# ベクトル化されたファイルを更新
embedding.update_embedding()

usr_prompt = ""
# query_o1_prompt.txtをロード
with open("manual/query_o1_prompt.txt", "r", encoding="utf-8") as f:
    usr_prompt = f.read()

prompt = embedding.create_rag_prompt(usr_prompt, token_limit=24000)

prompt += "\n# System Prompt\n" + ask.SYSTEM_PROMPT + "\n# Instructions\n" + usr_prompt

# o1_prompt.txt に書き込む
with open("o1_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)