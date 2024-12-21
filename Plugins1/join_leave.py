from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, User

from config import FSUB, RFSUB
from Database.pending_request_db import delete_user
from Database.settings import get_settings
from Plugins.start import start_markup
from templates import LEAVE_MESSAGE

if RFSUB and RFSUB[0]:
    FSUB = FSUB + RFSUB 


@Client.on_message(filters.chat(FSUB) & (filters.new_chat_members | filters.left_chat_member))
async def jl(_: Client, m: Message):
    settings = await get_settings()
    markup = await start_markup(_)
    if m.new_chat_members:
        users: List[User] = m.new_chat_members
        for user in users:
            await delete_user(user.id, m.chat.id)
        """
        if not settings['join']:
            return
        try:
            if JOIN_IMAGE:
                await _.send_photo(user.id, JOIN_IMAGE, caption=JOIN_MESSAGE, reply_markup=markup)
            else:
                await _.send_message(user.id, JOIN_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
        """

    else:
        if not settings['leave']:
            return
        try:
            user: User = m.left_chat_member
            # if LEAVE_IMAGE:
            #     await _.send_photo(user.id, LEAVE_IMAGE, caption=LEAVE_MESSAGE, reply_markup=markup)
            # else:
            #     await _.send_message(user.id, LEAVE_MESSAGE, reply_markup=markup)
            await _.send_voice(user.id, 'Voice/uff.ogg', caption=LEAVE_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
