from . import db

db = db.forward_data

async def insert_user_data(msg_id:int, user_id: int):
    await db.insert_one({"user_id": user_id, "msg_id": msg_id})
    return

async def get_and_delete(msg_id: int):
    to_return = None
    if data := await db.find_one_and_delete({"msg_id": msg_id}):
        to_return = data["user_id"]

    return to_return