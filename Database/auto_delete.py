from . import db

db = db.auto_delete

async def update(user_id, dic):
    await db.update_one({'user_id': user_id}, {'$set': {'dic': dic}}, upsert=True)

async def get(user_id):
    x = await db.find_one({'user_id': user_id})
    if x:
        return x['dic']
    return {}

async def get_all():
    # Fetching only active users who have enabled auto delete
    x = db.find({"auto_delete_status": "active"})
    x = await x.to_list(length=None)
    return [y['user_id'] for y in x]
