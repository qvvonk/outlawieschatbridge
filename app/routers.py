from __future__ import annotations
from typing import TYPE_CHECKING
from aiogram import Router
from discord.utils import escape_markdown
from discord import Embed
from aiogram.types import ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator

if TYPE_CHECKING:
    from .main import App
    from aiogram.types import Message

router = Router()


@router.message(
    lambda m: m.text,
    lambda m, app: (m.chat.id, m.message_thread_id) in app.tg_to_ds_chats
)
async def send_to_ds(m: Message, app: App):
    mem = await app.tg.get_chat_member(m.chat.id, m.from_user.id)
    photo = await m.from_user.get_profile_photos()
    file = await app.tg.get_file(photo.photos[-1][0].file_id)
    url = f'https://api.telegram.org/file/bot{app.tg.token}/{file.file_path}'

    user_data = []
    if m.from_user.full_name:
        user_data.append(m.from_user.full_name)

    tag = None
    if isinstance(mem, ChatMemberMember):
        tag = mem.tag
    elif isinstance(mem, (ChatMemberOwner, ChatMemberAdministrator)):
        tag = mem.custom_title

    if tag:
        user_data.append(f'({tag})')

    embed = Embed(
        description=escape_markdown(m.text),
        color=0x2B2D31
    )

    embed.set_author(
        name=' '.join(user_data),
        url=f'https://t.me/{m.from_user.username}' if m.from_user.username else None,
        icon_url=url
    )

    embed.add_field(
        name="Original",
        value=f"*{escape_markdown(m.text)}*",
        inline=False,
    )
    await app.ds.get_channel(app.tg_to_ds_chats[(m.chat.id, m.message_thread_id)]).send(embed=embed)
