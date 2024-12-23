
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import ChatMemberUpdated

from config import FSUB, JOIN_IMAGE, RFSUB
from Database.pending_request_db import delete_user
from Database.settings import get_settings
from Plugins.start import start_markup
from templates import JOIN_MESSAGE, LEAVE_MESSAGE

if RFSUB and RFSUB[0]:
    FSUB = FSUB + RFSUB 

@Client.on_chat_member_updated()
async def idk(c: Client, j: ChatMemberUpdated):
    settings = await get_settings()
    if not (settings.get('join') or settings['leave']):
        return
    chat_id = j.chat.id
    markup = await start_markup(c)

    if member := j.new_chat_member:
        await delete_user(member.user.id, chat_id)

        if not settings['join']:
            return
        try:
            if JOIN_IMAGE:
                await c.send_photo(member.user.id, JOIN_IMAGE, caption=JOIN_MESSAGE, reply_markup=markup)
            else:
                await c.send_message(member.user.id, JOIN_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
    elif member := j.old_chat_member:
        print(member)
        try:
            if member.status != CMS.LEFT:
                return
        except:
            pass
        try:
            # if LEAVE_IMAGE:
            #     await c.send_photo(member.id, LEAVE_IMAGE, caption=LEAVE_MESSAGE, reply_markup=markup)
            # else:
            #     await c.send_message(member.id, LEAVE_MESSAGE, reply_markup=markup)
            await c.send_voice(member.user.id, 'Voice/uff.ogg', caption=LEAVE_MESSAGE, reply_markup=markup)
        except Exception as e:
            print(e)
    
    else:
        print("This update is missing new chat member or old chat member attribute")
        return
