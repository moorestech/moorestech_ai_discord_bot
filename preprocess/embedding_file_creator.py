from util import embedding
from util import token_counter

# ベクトル化されたファイルを更新
#embedding.update_embedding()

print(token_counter.get_token_count(
    "私はペンが好きです。"
))