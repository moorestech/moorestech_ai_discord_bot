from chat_bot import ask
from mooresmaster import master_rag_prompt

# master.txtをロード
usr_prompt = ""
with open("master.txt", "r", encoding="utf-8") as f:
    usr_prompt = f.read()

prompt = master_rag_prompt.create_master_rag()

prompt += "\n# System Prompt\n" + ask.SYSTEM_PROMPT + "\n# Instructions\n" + usr_prompt

# o1_prompt.txt に書き込む
with open("o1_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)