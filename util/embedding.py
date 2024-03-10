import json
import numpy as np
from openai import OpenAI
from preprocess import cs_file

EMBEDDING_PATH = "../moorestech-embedding.json"

client = OpenAI()


# インデックスを更新する
def update_embedding():
    moorestech_embedding = json.load(open(EMBEDDING_PATH, 'r', encoding='utf-8'))

    # 全てのチェックフラグをFalseにする
    for embedding in moorestech_embedding:
        embedding['checked'] = False

    for file in cs_file.get_cs_files():

        # すでにベクトル化されているかをチェック
        is_checked = False
        for embedding in moorestech_embedding:
            # 相対パス、ファイル内容が一致していればスキップ
            if embedding['relative_path'] == file['relative_path'] and embedding['content'] == file['content']:
                embedding['checked'] = True
                is_checked = True
                break
        if is_checked:
            continue

        # ここでベクトル化を行う
        try:
            res = client.embeddings.create(
                model='text-embedding-ada-002',
                input=file['content']
            )
        except Exception as e:
            print("error " + file['actual_path'] + " : " + str(e))
            continue

        print("success " + file['actual_path'])

        # ベクトルをデータベースに追加
        moorestech_embedding.append({
            'file_name': file['file_name'],
            'relative_path': file['relative_path'],
            'content': file['content'],
            'embedding': res.data[0].embedding,
            'checked': True
        })

    # チェックフラグがFalseのものを削除
    moorestech_embedding = [embedding for embedding in moorestech_embedding if embedding['checked']]

    # ファイルに保存
    with open(EMBEDDING_PATH, 'w', encoding='utf-8') as f:
        json.dump(moorestech_embedding, f, ensure_ascii=False)

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def search_embedding(query, count=10):
    moorestech_embedding = json.load(open(EMBEDDING_PATH, 'r', encoding='utf-8'))

    client = OpenAI()

    # クエリをベクトル化
    res = client.embeddings.create(
        model='text-embedding-ada-002',
        input=query
    )
    q_embeddings = res.data[0].embedding

    # ベクトルを比較
    results = []
    for embedding in moorestech_embedding:

        similarity = cos_sim(q_embeddings, embedding['embedding'])

        results.append({
            'cs_data': embedding,
            'similarity': similarity
        })

    # 類似度でソート
    results.sort(key=lambda x: x['similarity'], reverse=True)

    return results[:count]
