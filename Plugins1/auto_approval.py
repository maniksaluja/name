from pyrogram import Client, filters
from pyrogram.errors import (PeerIdInvalid, UserAlreadyParticipant,
                             UserIsBlocked)
from pyrogram.types import ChatJoinRequest
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from config import JOIN_IMAGE, MUST_VISIT_LINK, RFSUB, TUTORIAL_LINK
from Database.pending_request_db import delete_user, insert_user
from Database.settings import get_settings
from Database.users import add_user_2
from Plugins.start import get_chats
from templates import JOIN_MESSAGE


@Client.on_chat_join_request(filters.chat(RFSUB))
async def cjr(_: Client, r: ChatJoinRequest):
    chat = r.chat
    userId = r.from_user.id
    
    await insert_user(userId, chat.id) #fail safe insert user at starting so even if the approving fails the user can still access the contents

    link = (await get_chats(_))[1][0]
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
    settings = await get_settings()
    if not settings['auto_approval']:
        return


    try:
        # Approve the chat join request
        is_success = await r.approve()
        # Send a welcome message to the user

        if not is_success:
            print(f"Failed to approve join request of the user: {userId} in chat: {chat.id}")
            return
            
        await delete_user(userId, chat.id) #Delete the pending request user from db as the join request is accepted successfully

        if JOIN_IMAGE:
            await _.send_photo(r.from_user.id, JOIN_IMAGE, caption=JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        else:
            await _.send_message(r.from_user.id, JOIN_MESSAGE.format(r.from_user.mention), reply_markup=markup)
        await add_user_2(r.from_user.id)
    except UserAlreadyParticipant:
        pass  # Ignore if user is already a participant
    except UserIsBlocked:
        print(f"Cannot send message to user {r.from_user.id}, as they have blocked the bot.")
    except PeerIdInvalid:
        print(f"Cannot send message to user {r.from_user.id}, invalid peer ID.")
    except Exception as e:
        print(e)
