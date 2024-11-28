import asyncio
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
    result = asyncio.run(ask.run_ask_ai_stream(response_message, question))

keep_alive()
bot.run(os.environ["DISCORD_BOT_TOKEN"])
