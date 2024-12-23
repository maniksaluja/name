
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from config import FSUB_1, JOIN_IMAGE, MUST_VISIT_LINK, TUTORIAL_LINK
from Database.pending_request_db import delete_user
from Database.settings import get_settings
from Plugins.start import get_chats
from templates import JOIN_MESSAGE, LEAVE_MESSAGE


@Client.on_chat_member_updated(filters.chat(FSUB_1))
async def idk(c: Client, j: ChatMemberUpdated):
    settings = await get_settings()
    if not (settings.get('join') or settings['leave']):
        return
    chat_id = j.chat.id
    link = (await get_chats(c))[1][0]
    markup = IKM(
      [
        [
          IKB("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=link),
          IKB("ᴄᴏᴅᴇ ʟᴀɴɢᴜᴀɢᴇ", url=MUST_VISIT_LINK)
        ],
        [
          IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)
        ]
      ]
    )
    if member := j.new_chat_member:
        await delete_user(member.user.id, chat_id)

        # if not settings['join']:
        #     return
        # try:
        #     if JOIN_IMAGE:
        #         await c.send_photo(member.user.id, JOIN_IMAGE, caption=JOIN_MESSAGE.format(member.user.mention), reply_markup=markup)
        #     else:
        #         await c.send_message(member.user.id, JOIN_MESSAGE.format(member.user.mention), reply_markup=markup)
        # except Exception as e:
        #     print("In join_leave:\n"+e)
    elif member := j.old_chat_member:
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
