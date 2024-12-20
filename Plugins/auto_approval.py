from pyrogram import Client, filters
from pyrogram.errors import (PeerIdInvalid, UserAlreadyParticipant,
                             UserIsBlocked)
from pyrogram.types import ChatJoinRequest

from Database.pending_request_db import delete_user, insert_user
from Database.settings import get_settings

from .start import FSUB_1


@Client.on_chat_join_request(filters.chat(FSUB_1))
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
        await client.send_message(userId, "Hi")
    except UserAlreadyParticipant:
        pass  # Ignore if user is already a participant
    except UserIsBlocked:
        print(f"Cannot send message to user {userId}, as they have blocked the bot.")
    except PeerIdInvalid:
        print(f"Cannot send message to user {userId}, invalid peer ID.")
    except Exception as e:
        print(f"Unexpected error: {e}")
