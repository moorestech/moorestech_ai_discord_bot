import hashlib
import json
import numpy as np
from openai import OpenAI
from util import token_counter , cs_file

EMBEDDING_PATH = "moorestech-embedding.json"

client = OpenAI()


# インデックスを更新する
def update_embedding():
    moorestech_embedding = json.load(open(EMBEDDING_PATH, 'r', encoding='utf-8'))

    # 全てのチェックフラグをFalseにする
    for embedding in moorestech_embedding:
        embedding['checked'] = False

    for file in cs_file.get_pjt_files():

        # すでにベクトル化されているかをチェック
        is_checked = False
        for embedding in moorestech_embedding:
            # 相対パス、ファイル内容が一致していればスキップ
            embedding_sha256 = hashlib.sha256(embedding['content'].encode()).hexdigest()
            file_sha256 = hashlib.sha256(file['content'].encode()).hexdigest()
            if embedding['relative_path'] == file['relative_path'] and embedding_sha256 == file_sha256:
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

        file_name = file['file_name']
        relative_path = file['relative_path']
        content = file['content']

        # ベクトルをデータベースに追加
        moorestech_embedding.append({
            'file_name': file_name,
            'file_name_token_count': token_counter.get_token_count(file_name),
            'relative_path': relative_path,
            'relative_path_token_count': token_counter.get_token_count(relative_path),
            'content': content,
            'content_token_count': token_counter.get_token_count(content),
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


def search_embedding(query, count=10, force_include_file_name=[]):
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

        # force_include_classで指定されている名前がクラス名に含まれている場合はsimilarityを1にする
        for file_name in force_include_file_name:
            if file_name in embedding['file_name']:
                similarity = 1
                break

        results.append({
            'cs_data': embedding,
            'similarity': similarity
        })

    # 類似度でソート
    results.sort(key=lambda x: x['similarity'], reverse=True)

    return results[:count]


def create_rag_prompt(query, token_limit=5000, force_include_file_name=[]):
    results = search_embedding(query, 10000, force_include_file_name)
    current_token_count = 0
    rag_cs_data = []

    for result in results:
        cs_data = result['cs_data']
        content_token_count = cs_data['content_token_count']
        relative_path_token_count = cs_data['relative_path_token_count']

        if current_token_count + content_token_count + relative_path_token_count > token_limit:
            break

        rag_cs_data.append(cs_data)
        current_token_count += content_token_count + relative_path_token_count

    # プロンプトの最後の方がより関係する情報なので逆順にする
    rag_cs_data.reverse()

    rag_prompt = ""
    for cs_data in rag_cs_data:
        current_rag = cs_data['relative_path'] + "\n"
        current_rag += "```cs\n" + cs_data['content'] + "\n```\n\n"

        rag_prompt = rag_prompt + current_rag

        print("Rag File: ", cs_data['file_name'])

    return rag_prompt
