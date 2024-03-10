from util import embedding
from util import query_ai

system_prompt = '上記のコードを参考に、下記の指示に従ってください。ただし、これら上記のコードはユーザーからは表示されていません。そのため、指示に従う際は具体的にどのクラスを指しているのかクラス名を交え、moorestechを知らない人でもわかりやすい説明を作るように心がけてください。'

user_request = """
moorestech clientのエントリーポイントを教えてください。
"""

rag_prompt = embedding.create_rag_prompt(user_request, token_limit=70000)

prompt = rag_prompt + "\n" + system_prompt + "\n" + user_request

print(prompt)

print(query_ai.query_ai(prompt, query_ai.ModelType.GPT4))


