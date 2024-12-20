from pyrogram import Client, filters
from pyrogram.errors import (PeerIdInvalid, UserAlreadyParticipant,
                             UserIsBlocked)
from pyrogram.types import ChatJoinRequest

from config import RFSUB
from Database.pending_request_db import delete_user, insert_user
from Database.settings import get_settings


@Client.on_chat_join_request(filters.chat(RFSUB))
async def chat_join_request_handl(client: Client, request: ChatJoinRequest):
    """
    Automatically approve chat join requests if auto-approval is enabled.
    """
    chat = request.chat
    userId = request.from_user.id
    print(userId)
    await insert_user(userId, chat.id) #fail safe insert user at starting so even if the approving fails the user can still access the contents

    settings = await get_settings()
    if not settings['auto_approval']:
        return

    try:
        # Approve the chat join request
        iSapproved = await request.approve()
        print(iSapproved)
        if not iSapproved:
            print(f"Failed to approve join request of the user: {userId} in chat: {chat.id}")
            return
            
        await delete_user(userId, chat.id) #Delete the pending request user from db as the join request is accepted successfully

        # Send a welcome message to the user
        await client.send_message(request.from_user.id, "Hi")
    except UserAlreadyParticipant:
        pass  # Ignore if user is already a participant
    except UserIsBlocked:
        print(f"Cannot send message to user {request.from_user.id}, as they have blocked the bot.")
    except PeerIdInvalid:
        print(f"Cannot send message to user {request.from_user.id}, invalid peer ID.")
    except Exception as e:
        print(f"Unexpected error: {e}")
