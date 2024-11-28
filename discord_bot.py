import os
import asyncio
import threading
import queue
from chat_bot import ask
from discord import app_commands
import discord

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を取得する権限

# Botをインスタンス化
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print("Bot is ready!")

@tree.command(name='ask', description='moorestechのコードについて聞けます。')
@discord.app_commands.describe(question="質問内容")
async def test(interaction: discord.Interaction, question: str):
    print("[ask] question:", question)
    await interaction.response.defer()

    response_message = await interaction.followup.send("回答を生成しています...")

    collected_response = ""
    response_queue = queue.Queue()
    response_complete = asyncio.Event()

    # 定期的にメッセージを更新するタスクを定義
    async def update_message():
        nonlocal collected_response
        print("Starting update task")
        while not response_complete.is_set():
            print("Updating message")
            # キューから新しいチャンクを取得
            while not response_queue.empty():
                chunk = response_queue.get()
                collected_response += chunk
            # 2000字に収まるように調整
            display_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + collected_response[:2000]
            try:
                await response_message.edit(content=display_response)
            except Exception as e:
                print("Error updating message:", e)
            await asyncio.sleep(0.2)

        # 最後の更新
        while not response_queue.empty():
            chunk = response_queue.get()
            collected_response += chunk
        display_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + collected_response[:2000]
        try:
            await response_message.edit(content=display_response)
        except Exception as e:
            print("Error updating message:", e)

    # メッセージ更新タスクをバックグラウンドで開始
    update_task = asyncio.create_task(update_message())

    # ブロッキング処理を別スレッドで実行
    def blocking_collect_response():
        try:
            # 新しいイベントループを作成
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async def async_collect():
                async for chunk in ask.ask_ai_stream(question):
                    response_queue.put(chunk)
            loop.run_until_complete(async_collect())
            loop.close()
        except Exception as e:
            print("Error in streaming response:", e)
        finally:
            # 完了を通知
            response_complete.set()

    thread = threading.Thread(target=blocking_collect_response)
    thread.start()

    # 完了イベントを待機
    await response_complete.wait()

    # タスクをキャンセルして最終更新
    await update_task

    # 最終的なメッセージを更新（念のため）
    display_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + collected_response[:2000]
    await response_message.edit(content=display_response)

keep_alive()
bot.run(os.environ["DISCORD_BOT_TOKEN"])
