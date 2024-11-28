import os
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
    async for chunk in ask.ask_ai_stream(question):
        collected_response += chunk
        # 2000字に収まるように調整
        display_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + collected_response[:2000]
        await response_message.edit(content=display_response)

keep_alive()
bot.run(os.environ["DISCORD_BOT_TOKEN"])
