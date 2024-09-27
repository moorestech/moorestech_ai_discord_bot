from chat_bot import ask
from util import embedding

usr_prompt = "moorestechのクライアントサイドでインベントリ付きのブロックをクリックしてもそのブロックのインベントリが開きません。考えられる原因を教えて下さい。"

prompt = embedding.create_rag_prompt(usr_prompt, token_limit=20000)

prompt += "\n# System Prompt\n" + ask.SYSTEM_PROMPT + "\n# Instructions\n" + usr_prompt