"""
DISCORD.PY 2.0 BOT ONLY FOR ONE GUILD
✅❌
cd /D D:\\sus\\py\\jett
"""
# ==============================================================================

from typing import Optional

import discord
from discord import app_commands
import j_token
import j_mechanics

import datetime
from humanfriendly import format_timespan, parse_timespan

# ==============================================================================

MY_GUILD = discord.Object(id=700246237244555334)  # Parad0x server id
MY_TOKEN = j_token.jett_TOKEN()  # Jett#2399 token

# ==============================================================================

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)  # command tree for sync

    async def setup_hook(self):  # copy the global commands over to your guild
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

# ==============================================================================
"""
ON READY
"""
@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


# ==============================================================================
"""
EMBED:
    only for staff
"""
@client.tree.command()
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(title="Заголовок окна", 
                       description="Описание окна", 
                       image_url="Ссылка на изображение внутри окна под описанием")

async def send_embed(interaction: discord.Interaction, 
                     title: str, 
                     description: Optional[str] = None, 
                     image_url: Optional[str] = None):
    """Простой конструктор окна-вставки"""

    emb = discord.Embed(title=title, description=description, color=0x2f3136)  # make embed
    emb.set_image(url=image_url)  # image
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
    emb.timestamp = message.created_at

    await interaction.response.send_message(embed=emb)  # sending embed



# ==============================================================================
"""
VOTING:
    for all users
"""
@client.tree.command()
@app_commands.describe(description="Твоё предложение по серверу", 
                       image_url="Ссылка на одно изображение, если тебе надо")

async def vote(interaction: discord.Interaction,
               description: str, 
               image_url: Optional[str] = None):
    """Предложение/опрос относительно сервера на любую тему """

    emb = discord.Embed(title=f"Предложение #{j_mechanics.vote_number_mecha()}", description=description, color=0x2f3136)
    emb.set_image(url=image_url)  # image
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
    emb.timestamp = message.created_at

    await interaction.response.send_message("Предложение создано!", ephemeral=True)  # sending message if ok

    channel = client.get_channel(759848748787695666)  # special channel for votes
    message = await channel.send(embed=emb)  # sending embed
    await message.add_reaction("🔼")  # adding reaction up to message
    await message.add_reaction("🔽")  # adding reaction down to message



# ==============================================================================
"""
MUTE:
    for mods and staff
"""
@client.tree.command()
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, которого хочешь замутить", 
                       time="Время в формате 1s/1m/1h/1d",
                       reason="Причина мута")

async def mute(interaction: discord.Interaction,
               member: discord.Member, 
               time: str, 
               reason: Optional[str] = "Причина не указана"):
    """Мут пользователя через таймаут"""

    time = parse_timespan(time)  # converting time
    await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)  # mute user

    emb = discord.Embed(title='Мут!', 
                        description=f'{member.mention} poly4aet myt na {format_timespan(time)}', 
                        color=0xff0800)
    emb.add_field(name='Причина', value=f'\n**`{reason}`**')  # reason
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
    emb.timestamp = message.created_at

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(766935673478447145).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
UNMUTE:
    for mods and staff
"""
@client.tree.command()
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, которого хочешь размутить")

async def unmute(interaction: discord.Interaction,
                 member: discord.Member):
    """Анмут пользователя через таймаут"""

    await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=1))  # unmute user

    emb = discord.Embed(title='Анмут!', 
                        description=f'{member.mention} теперь может говорить', 
                        color=0xff0800)
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
    emb.timestamp = message.created_at

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(766935673478447145).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
WARN:
    for mods and staff
"""
@client.tree.command()
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, который получит предупреждение", 
                       reason="Причина предупреждения")

async def warn(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str] = "Причина не указана"):
    """Варн пользователя (4 предупреждения = мут на 6 часов)"""

    warns_count, more_than_two = j_mechanics.warn_mecha(member.id)  # how many warns
    if more_than_two:  # if user has 4 warns
        await member.timeout(discord.utils.utcnow()+datetime.timedelta(hours=6), reason="Слишком много предупреждений")  # mute user
        emb = discord.Embed(title='Мут!', 
                            description=f'{member.mention} получает мут на 6 часов за предупреждения', 
                            color=0xff0800)
        emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
        emb.timestamp = message.created_at
    else:
        emb = discord.Embed(title='Предупреждение!', 
                            description=f'{member.mention} получает своё {warns_count} предупреждение', 
                            color=0xff0800)
        emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
        emb.timestamp = message.created_at

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(766935673478447145).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
REPORT MESSAGE:
    for all users
    context menu
"""
@client.tree.context_menu(name='Репорт модерам')
async def report_message(interaction: discord.Interaction, 
                         message: discord.Message):
    await interaction.response.send_message(f'Твоя жалоба на {message.author.mention} передана модераторам :3', ephemeral=True)

    emb = discord.Embed(title='Репорт на сообщение')
    if message.content:
        emb.description = message.content

    emb.set_author(name=f"Провинившийся: {message.author}", icon_url=message.author.display_avatar)  # who was reported
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it
    emb.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Перейти к сообщению', style=discord.ButtonStyle.url, url=message.jump_url))

    await interaction.guild.get_channel(758279107006955531).send(embed=emb, view=url_view)  # sending embed to moderator channel



# ==============================================================================
#                 RUN
#                 RUN
#                 RUN
#                 RUN
#                 RUN
client.run(j_token.jett_TOKEN())
#                 RUN
#                 RUN
#                 RUN
#                 RUN
#                 RUN