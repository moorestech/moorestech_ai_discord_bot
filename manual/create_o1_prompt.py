from chat_bot import ask
from mooresmaster import master_rag_prompt
from util import embedding

# master.txtをロード
usr_prompt = "MinerMiningTestクラスを参考に、VanillaGearMinerComponentのテストコードを記述してください。"

prompt = embedding.create_rag_prompt(usr_prompt, token_limit=20000)

prompt += "\n# System Prompt\n" + ask.SYSTEM_PROMPT + "\n# Instructions\n" + usr_prompt

# o1_prompt.txt に書き込む
with open("o1_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)