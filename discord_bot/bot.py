import os

from discord.ext import commands
from discord import app_commands
import discord
from chat_bot import ask

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
    ai_response = ask.ask_ai(question)
    final_response = "# 質問\n\n" + question + "\n\n# 回答\n\n" + ai_response
    await interaction.followup.send(final_response)


bot.run(os.environ["DISCORD_BOT_TOKEN"])
