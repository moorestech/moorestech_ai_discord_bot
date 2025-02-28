# moorestechのDiscordで使っているbot

## コード簡単解説

### chat_botフォルダ
Discordのaskコマンドで使用する、ストリーム対応のチャットボット処理

### manualフォルダ
pythonプロジェクトをクローンして、手動で実行をするためのpythonコードが入っています。
大抵はupdate_embedding.pyを起動して、埋込行列の更新を行っています

### uitlフォルダ
埋め込みの更新、不要なC#ファイルの除去、トークン数のカウント、AIクエリの実行など、Discordボットの根幹となる部分の処理を書いています。