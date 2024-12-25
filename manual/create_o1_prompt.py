from chat_bot import ask
from mooresmaster import master_rag_prompt
from util import embedding

# ベクトル化されたファイルを更新
embedding.update_embedding()

usr_prompt = ""
# query_o1_prompt.txtをロード
with open("manual/query_o1_prompt.txt", "r", encoding="utf-8") as f:
    usr_prompt = f.read()

rag_reference = ""
with open("manual/rag_reference.txt", "r", encoding="utf-8") as f:
    rag_reference = f.read()

# force_include_file_name.txtを読み込んで、行ごとの配列にする
force_include_file_name = []
with open("manual/force_include_file_name.txt", "r", encoding="utf-8") as f:
    force_include_file_name = f.read().splitlines()

prompt = embedding.create_rag_prompt(rag_reference + usr_prompt, token_limit=95000, force_include_file_name=force_include_file_name)

prompt += ("コードを書く場合はコメント、空白、タブ、改行は本のコードと全く同じにしてください。適切な差分を維持するため、必要箇所以外は編集しないでください。"
           "また、コピペしやすいように、差分表記ではなく、コードそのものを記述してください。"
           "\n# Instructions\n") + usr_prompt

# o1_prompt.txt に書き込む
with open("manual/o1_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)