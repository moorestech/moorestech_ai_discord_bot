import openai
import os
import json

from preprocess import cs_file

EMBEDDING_PATH = "../moorestech-embedding.json"

moorestech_embedding = json.load(open(EMBEDDING_PATH, 'r', encoding='utf-8'))

# 全てのチェックフラグをFalseにする
for embedding in moorestech_embedding:
    embedding['checked'] = False

for file in cs_file.get_cs_files():

    # すでにベクトル化されているかをチェック
    for embedding in moorestech_embedding:
        # 相対パス、ファイル内容が一致していればスキップ
        if embedding['relative_path'] == file['relative_path'] and embedding['content'] == file['content']:
            embedding['checked'] = True
            break

    # ここでベクトル化を行う
    try:
        res = openai.Embedding.create(
            model='text-embedding-ada-002',
            input=file['content']
        )
    except Exception as e:
        print("error " + file['actual_path'] + " : " + str(e))
        continue

    # ベクトルをデータベースに追加
    moorestech_embedding.append({
        'file_name': file['file_name'],
        'relative_path': file['relative_path'],
        'content': file['content'],
        'embedding': res['data'][0]['embedding'],
        'checked': True
    })


# チェックフラグがFalseのものを削除
moorestech_embedding = [embedding for embedding in moorestech_embedding if embedding['checked']]

# ファイルに保存
with open(EMBEDDING_PATH, 'w', encoding='utf-8') as f:
    json.dump(moorestech_embedding, f, ensure_ascii=False)
