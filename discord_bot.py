import discord
import os

from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import io

from WoW.wow_statistics import get_mplus_stats
from albion_market.albion_api import percent_of_items
from currency_parser import average_usd_rate

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD_ID = discord.Object(id=1204033615588229151)

class Client(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def setup_hook(self):
        await self.tree.sync(guild=GUILD_ID)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')


intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents, command_prefix='!')

user_profiles = {}

@client.event
async def on_ready():
    await client.tree.sync(guild=GUILD_ID)
    print(f"{client.user} подключен.")


@client.tree.command(name='hello', description='Say hello!', guild=GUILD_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello!')


@client.tree.command(name='usd', description='average_usd_rate', guild=GUILD_ID)
async def pong(interaction: discord.Interaction):
    result = await average_usd_rate()
    await interaction.response.send_message(result)

@client.tree.command(name='prices', description='prices for trading', guild=GUILD_ID)
async def pong(interaction: discord.Interaction):
    profit_list = percent_of_items()
    output = "\n".join(profit_list)

    file = discord.File(fp=io.StringIO(output), filename="profit_list.txt")
    await interaction.response.send_message("Список профитных предметов:", file=file)

@client.tree.command(name='set_wow', description='Сохранить своего WoW-персонажа', guild=GUILD_ID)
@app_commands.describe(name="Имя персонажа", realm="Сервер", region="Регион (eu/us/...)")
async def set_wow(interaction: discord.Interaction, name: str, realm: str, region: str = "eu"):
    user_profiles[interaction.user.id] = {
        "name": name,
        "realm": realm.lower(),
        "region": region
    }
    await interaction.response.send_message(f"✅ Профиль {name} ({realm}-{region}) сохранён!", ephemeral=True)

@client.tree.command(name='mplus', description='Показать Mythic+ статистику сохранённого персонажа', guild=GUILD_ID)
async def mplus(interaction: discord.Interaction):
    profile = user_profiles.get(interaction.user.id)
    if not profile:
        await interaction.response.send_message("❌ Сначала используй `/set_wow`, чтобы сохранить профиль.", ephemeral=True)
        return

    data = get_mplus_stats(profile["region"], profile["realm"], profile["name"])
    if not data:
        await interaction.response.send_message("⚠ Не удалось получить данные. Проверь имя и сервер.")
        return

    rating = data["mythic_plus_scores_by_season"][0]["scores"]["all"]
    best_runs = data["mythic_plus_best_runs"]

    msg = f"**{data['name']} ({profile['realm'].title()}-{profile['region'].upper()})**\n"
    msg += f"Mythic+ Рейтинг: **{rating}**\n"
    msg += f"Лучшие проходки:\n"

    for run in best_runs[:8]:
        dungeon = run["dungeon"]
        level = run["mythic_level"]
        minutes = run["clear_time_ms"] // 60000
        msg += f"- +{level} {dungeon} за {minutes} мин.\n"

    await interaction.response.send_message(msg)

@client.tree.command(name='dota_statistic', description='Dota players statistic', guild=GUILD_ID)
async def dota_statistic(interaction: discord.Interaction):
    await interaction.response.defer()  # если нужно подольше ждать ответ

    matches = get_recent_matches(steam32_id, limit=5)
    if not matches:
        await interaction.followup.send("❌ Не удалось получить матчи или их нет.")
        return

    await interaction.response.send_message(msg)


if __name__ == '__main__':
    client.run(TOKEN)