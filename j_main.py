"""
DISCORD.PY 2.0 BOT ONLY FOR parad0x
cd /D D:\\sus\\py\\jett

pip install discord
pip install humanfriendly
"""
# ==============================================================================

from typing import Optional

import json
import discord
from discord.ui import Select, ChannelSelect, View
from discord import app_commands
from discord import Spotify
import j_token
import j_mechanics

import datetime
from humanfriendly import format_timespan, parse_timespan   

import urllib.request

# ==============================================================================

MY_GUILD = discord.Object(id=1097987434253385810)  # parad0x server id
MY_TOKEN = j_token.mama_TOKEN()  # bot's token

# ==============================================================================

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)  # command tree for sync

    async def setup_hook(self):  # copy the global commands over to your guild
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.all()
intents.members = True
client = MyClient(intents=intents)


# ==============================================================================
"""
ON READY
"""
@client.event
async def on_ready():
    print(f"Logged as {client.user} (id: {client.user.id})")
    guild = client.get_guild(MY_GUILD)
    await client.change_presence(status=discord.Status.online, 
                              activity=discord.Streaming(name="VALORANT", url="https://www.twitch.tv/3wpty"))



# ==============================================================================
"""
EMBED:
    only for staff
"""
@client.tree.command(name="embed")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(title="Заголовок окна", 
                       description="Описание окна", 
                       image_url="Ссылка на изображение внутри окна под описанием")

async def cmd_send_embed(interaction: discord.Interaction, 
                     title: str, 
                     description: Optional[str] = None, 
                     image_url: Optional[str] = None):
    """ADMIN ONLY // Создать окно-вставку """

    emb = discord.Embed(title=title, description=description, color=0x2f3136)  # make embed
    emb.set_image(url=image_url)  # image
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    await interaction.response.send_message(embed=emb)  # sending embed



# ==============================================================================
"""
VOTING:
    for all users
"""
@client.tree.command(name="vote")
@app_commands.describe(description="Твоё предложение по серверу", 
                       image_url="Ссылка на одно изображение, если тебе надо")

async def cmd_vote(interaction: discord.Interaction,
               description: str, 
               image_url: Optional[str] = None):
    """Добавить предложение/опрос относительно сервера на любую тему"""

    emb = discord.Embed(title=f"Предложение #{j_mechanics.vote_number_mecha()}", description=description, color=0x2f3136)
    emb.set_image(url=image_url)  # image
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    await interaction.response.send_message("Предложение создано!", ephemeral=True)  # sending message if ok

    channel = client.get_channel(1098682161101545532)  # special channel for votes
    message = await channel.send(embed=emb)  # sending embed
    await message.add_reaction("🔼")  # adding reaction up to message
    await message.add_reaction("🔽")  # adding reaction down to message



# ==============================================================================
"""
MUTE:
    for mods and staff
"""
@client.tree.command(name="mute")
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, которого хочешь замутить", 
                       time="Время в формате 1s/1m/1h/1d",
                       reason="Причина мута")

async def cmd_mute(interaction: discord.Interaction,
               member: discord.Member, 
               time: str, 
               reason: Optional[str] = "Причина не указана"):
    """MOD ONLY // Выдать мут пользователю через таймаут"""

    time = parse_timespan(time)  # converting time
    await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)  # mute user

    emb = discord.Embed(title='Мут!', 
                        description=f'{member.mention} poly4aet myt na {format_timespan(time)}', 
                        color=0xff0800)
    emb.add_field(name='Причина', value=f'\n**`{reason}`**')  # reason
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(1098697565593145344).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
UNMUTE:
    for mods and staff
"""
@client.tree.command(name="unmute")
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, которого хочешь размутить")

async def cmd_unmute(interaction: discord.Interaction,
                 member: discord.Member):
    """MOD ONLY // Размутить пользователя через таймаут"""

    await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=1))  # unmute user

    emb = discord.Embed(title='Анмут!', 
                        description=f'{member.mention} теперь может говорить', 
                        color=0xff0800)
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(1098697565593145344).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
WARN:
    for mods and staff
"""
@client.tree.command(name="warn")
@app_commands.checks.has_permissions(view_audit_log=True)
@app_commands.describe(member="Чел, который получит предупреждение", 
                       reason="Причина предупреждения")

async def cmd_warn(interaction: discord.Interaction,
               member: discord.Member,
               reason: Optional[str] = "Причина не указана"):
    """MOD ONLY // Выдать предупреждение пользователю (4 предупреждения = мут на 6 часов)"""

    warns_count, more_than_two = j_mechanics.warn_mecha(member.id)  # how many warns
    if more_than_two:  # if user has 4 warns
        await member.timeout(discord.utils.utcnow()+datetime.timedelta(hours=6), reason="Слишком много предупреждений")  # mute user
        emb = discord.Embed(title='Мут!', 
                            description=f'{member.mention} получает мут на 6 часов за предупреждения', 
                            color=0xff0800)
        emb.add_field(name='Причина', value=f'\n**`{reason}`**')  # reason
        emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    else:
        emb = discord.Embed(title='Предупреждение!', 
                            description=f'{member.mention} получает своё {warns_count} предупреждение', 
                            color=0xff0800)
        emb.add_field(name='Причина', value=f'\n**`{reason}`**')  # reason
        emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    await interaction.response.send_message(embed=emb, ephemeral=True)  # sending message if ok
    message = await interaction.guild.get_channel(1098697565593145344).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
CREATING ROLE:
    for all users
"""
# @client.tree.command(name="add-custom-role")
# @app_commands.describe(name="Название твоей роли",
#                        color="Любой цвет роли в формате rrggbb (Пример: красный - `ff0000`, голубой - `6ed8f0`)")

# async def cmd_add_custom_role(interaction: discord.Interaction, 
#                       name: str, 
#                       color: str):
#     """Создать свою уникальную роль (своё название и цвет)"""


#     if color == "420":  # if no some of args

#         emb = discord.Embed(title=":warning:**Ошибка!**",
#                             description="Цвет указан неправильно",
#                             color=0xffcc4d)

#     else:  # if Ok
#         role_already_exist = j_mechanics.role_mecha(interaction.user.id)  # role already exist or not

#         if role_already_exist:  # if user already have custom role
#             role_id = j_mechanics.role_id_mecha(interaction.user.id)  # finding id of role from json file
#             role = interaction.guild.get_role(role_id)  # getting role object
#             role = await role.edit(name=name, color=int(f"0x{color}", 16), position=(len(interaction.guild.roles)-5))  # editing role
#             await interaction.user.add_roles(role)  # give role to the user


#         else:

#             role = await interaction.guild.create_role()  # creating role
#             role = await role.edit(name=name, color=int(f"0x{color}", 16), position=(len(interaction.guild.roles)-5))  # editing role
#             j_mechanics.role_id_mecha(interaction.user.id, role.id)  # save role id to json file
#             await interaction.user.add_roles(role)  # give role to the user

#         emb = discord.Embed(title='Роль сделана!', 
#                             description=f'{interaction.user.mention} сделал себе уникальную роль: <@&{role.id}>', 
#                             color=0x77b255)

#     emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

#     await interaction.response.send_message(embed=emb)  # sending embed
#     message = await interaction.guild.get_channel(1098697565593145344).send(embed=emb)  # sending embed to log channel




# ==============================================================================
"""
DELETING CREATED ROLE:
    for all users
"""
# @client.tree.command(name="remove-custom-role")
# @app_commands.describe(confirm="Напиши `yes` без кавычек для удаления роли")

# async def cmd_remove_custom_role(interaction: discord.Interaction, 
#                       confirm: str):
#     """Удалить свою уникальную роль (потом можно будет создать новую)"""

#     if confirm != "yes":  # if no some of args

#         emb = discord.Embed(title=":warning:**Ошибка!**",
#                             description="Напиши `yes` в поле **confirm** чтобы удалить кастомную роль",
#                             color=0xffcc4d)

#     else:  # if Ok
#         role_already_exist = j_mechanics.role_mecha(interaction.user.id)  # role already exist or not

#         if role_already_exist:  # if user already have custom role
#             role_id = j_mechanics.role_id_mecha(interaction.user.id)  # finding id of role from json file
#             role = interaction.guild.get_role(role_id)  # getting role object
#             await interaction.user.remove_roles(role)  # give role to the user

#             emb = discord.Embed(title='Роль удалена!', 
#                                 description=f'{interaction.user.mention} удалил свою уникальную роль', 
#                                 color=0x77b255)

#         else:

#             emb = discord.Embed(title=":warning:**Ошибка!**",
#                             description="У тебя нет кастомной роли",
#                             color=0xffcc4d)


#     emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

#     await interaction.response.send_message(embed=emb)  # sending embed
#     message = await interaction.guild.get_channel(1098697565593145344).send(embed=emb)  # sending embed to log channel



# ==============================================================================
"""
REPORT MESSAGE:
    for all users
    context menu
"""
@client.tree.context_menu(name="・ Репорт")
async def cmd_report_message(interaction: discord.Interaction, 
                         message: discord.Message):
    await interaction.response.send_message(f'Твоя жалоба на {message.author.mention} передана модераторам <3', ephemeral=True)

    date_created = f"{message.created_at.day}.{message.created_at.month}.{message.created_at.year} в {message.created_at.hour}:{message.created_at.minute}"
    emb = discord.Embed(title=f'Репорт на сообщение {message.author} \n(отправлено {date_created})', description=f"Провинившийся: {message.author}")
    if message.content:
        emb.description = message.content

    emb.set_thumbnail(url=message.author.display_avatar)  # who was reported
    emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Перейти к сообщению', style=discord.ButtonStyle.url, url=message   .jump_url))

    await interaction.guild.get_channel(1098701286968393739).send(embed=emb, view=url_view)  # sending embed to moderator channel






# ==============================================================================
"""
DM MESSAGE TO BOT:
    for all users
    direct message
"""
msg_dump_channel = 1098697356825866350

@client.event
async def on_message(message: discord.Message):
    channel = client.get_channel(msg_dump_channel)
    if (message.guild is None) and (message.author.id != 1125171114243543181):
        # if the channel is public at all, make sure to sanitize this first
        await channel.send(f'**{message.author}:** `{message.content}`')





# ==============================================================================
"""
CONNECT TO VOICE:
    only for staff
    voice
"""
@client.tree.command(name="cc")
@app_commands.checks.has_permissions(ban_members=True)

async def cmd_connect_to_voice(interaction: discord.Interaction):
    """ADMIN ONLY // Пригласить бота в войс"""


    channel = client.get_channel(interaction.user.voice.channel.id)
    voice_client = await channel.connect()

    await interaction.response.send_message(f'Подключилась к твоему каналу', ephemeral=True)



# ==============================================================================
"""
PAUSE/RESUME SONG:
    only for staff
    voice
"""
# @client.tree.command(name="pause")
# @app_commands.checks.has_permissions(ban_members=True)

# async def cmd_pause_voice(interaction: discord.Interaction):
#     """ADMIN ONLY // Остановить/продолжить музыку"""

#     voice_client = discord.utils.get(client.voice_clients)

#     if voice_client.is_connected():

#         if voice_client.is_paused():
#             voice_client.resume()

#         elif voice_client.is_playing():
#             voice_client.pause()

#     await interaction.response.send_message(f'Остановила/продолжила музыку', ephemeral=True)



# ==============================================================================
"""
STOP SONG:
    only for staff
    voice
"""
# @client.tree.command(name="stop")
# @app_commands.checks.has_permissions(ban_members=True)

# async def cmd_stop_voice(interaction: discord.Interaction):
#     """ADMIN ONLY // Выключить музыку"""

#     voice_client = discord.utils.get(client.voice_clients)

#     if voice_client.is_connected():
#         voice_client.stop()

#     await interaction.response.send_message(f'Выключила музыку', ephemeral=True)




# ==============================================================================
"""
DISCONNECT FROM VOICE:
    only for staff
    voice
"""
@client.tree.command(name="dc")
@app_commands.checks.has_permissions(ban_members=True)

async def cmd_disconnect_from_voice(interaction: discord.Interaction):
    """ADMIN ONLY // Кикнуть бота из войса"""

    voice_client = discord.utils.get(client.voice_clients)


    if voice_client.is_connected():

        if voice_client.is_playing():
            await voice_client.stop()
        
        await voice_client.disconnect()

    await interaction.response.send_message(f'Отключилась от твоего канала', ephemeral=True)
    



# ==============================================================================
"""
TWITCH ANNOUNCEMENT:
    only for staff
"""
# @client.tree.command(name="ttv-announcement")
# @app_commands.checks.has_permissions(ban_members=True)
# @app_commands.describe(title="Заголовок", 
#                        description="Описание", 
#                        image_url="Ссылка на изображение внутри окна под описанием")

# async def cmd_send_embed(interaction: discord.Interaction, 
#                      title: Optional[str] = "Эмпти запустил стрим!", 
#                      description: Optional[str] = j_mechanics.get_twitch_title_mecha(), 
#                      image_url: Optional[str] = "https://i.imgur.com/2hc6rHx.png"):
#                      # image_url: Optional[str] = "https://i.ibb.co/jyYyDcN/image-2024-09-14-214416177.png"):
#     """ADMIN ONLY // Анонс стрима Эмпти"""


#     emb = discord.Embed(title=title, description=description, color=0xff0084)  # make embed
#     emb.set_image(url=image_url)  # image
#     emb.set_footer(text=f"Инициатор: {interaction.user}", icon_url=interaction.user.display_avatar)  # who called it

#     await interaction.response.send_message(embed=emb)  # sending embed




# ==============================================================================
#                 RUN
#                 RUN
#                 RUN
client.run(j_token.mama_TOKEN())
#                 RUN
#                 RUN
#                 RUN
