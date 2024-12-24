watch = 69

from pyrogram import Client, filters
from pyrogram.types import Message

from config import FSUB_1, SUDO_USERS
from Database.users import add_user_2


@Client.on_message(filters.private, group=watch)
async def cwf(_, m: Message):
    if m.from_user and m.from_user.id in SUDO_USERS:
        return await add_user_2(m.from_user.id)
    await m.reply("**Have Any Queries? @CuteGirlTG**")
    await add_user_2(m.from_user.id)

@Client.on_message(filters.chat(FSUB_1))
async def give_reactionnn(_, m: Message):
    try:
        await m.react("👎")
    except Exception as e:
        print(f"Got error while giving reaction in bot 2: {e}")
    