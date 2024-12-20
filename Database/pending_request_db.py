#This file will store user id of incoming join request

from . import db

db = db.pending_request


async def insert_user(user_id: int, chat_id: int) -> None:
    print("Inserted")
    await db.insert_one({"user": user_id, "chat": chat_id})

async def delete_user(user_id: int, chat_id: int) -> None:
    await db.delete_one({"user": user_id, "chat": chat_id})

async def is_user_pending(user_id: int, chat_id: int) -> bool:
    try:
        return bool(await db.find_one({"user": user_id, "chat": chat_id}))
    except:
        return False #fail safe