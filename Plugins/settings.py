import asyncio
from time import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from config import LOG_CHANNEL_ID, LOG_CHANNEL_ID2, SUDO_USERS
from Database.settings import *

yes = '☑️'
no = '❌'

def log_chan(dic: dict):
    if x := dic.get("logs", None):
        if x == "both":
            return "Both"
        elif x == "l1":
            return f"Log Channel 1: {LOG_CHANNEL_ID}"
        else:
            return f"Log Channel 2: {LOG_CHANNEL_ID2}"
    return '❌'

def markup(dic):
    mark = IKM(
        [
            [
                IKB('𝘈𝘶𝘵𝘰 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭', callback_data='answer'),
                IKB(yes if dic.get('auto_approval', True) else no, callback_data='toggle_approval')
            ],
            [
                IKB('𝘞𝘦𝘭𝘤𝘰𝘮𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if dic.get('join', True) else no, callback_data='toggle_join')
            ],
            [
                IKB('𝘓𝘦𝘢𝘷𝘦 𝘔𝘚𝘎', callback_data='answer'),
                IKB(yes if dic.get('leave', True) else no, callback_data='toggle_leave')
            ],
            [
                IKB('𝘞𝘢𝘯𝘵 𝘐𝘮𝘢𝘨𝘦', callback_data='answer'),
                IKB(yes if dic.get('image', True) else no, callback_data='toggle_image')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘚𝘢𝘷𝘦', callback_data='answer'),
                IKB(yes if dic.get('auto_save', True) else no, callback_data='toggle_save')
            ],
            [
                IKB('𝘓𝘰𝘨 𝘊𝘩𝘢𝘯𝘯𝘦𝘭', callback_data='answer'),
                IKB(log_chan(dic), callback_data='toggle_logs')
            ],
            [
                IKB('𝘈𝘶𝘵𝘰 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘦', callback_data='answer'),
                IKB(dic.get('generate', 10), callback_data='toggle_gen')
            ]
        ]
    )
    return mark

dic = {}

@Client.on_message(filters.command('settings') & filters.user(SUDO_USERS))
async def settings(_, m):
    set = await get_settings()
    txt = '**IT Helps To Change Bot Basic Settings..**'
    mark = markup(set)
    ok = await m.reply(txt, reply_markup=mark)
    dic[m.from_user.id] = [ok, time()]
    
async def task():
    while True:
        rem = []
        for x in dic:
            if int(time() - dic[x][1]) > 120:
                try:
                    await dic[x][0].delete()
                except:
                    pass
                rem.append(x)
        for y in rem:
            del dic[y]
        await asyncio.sleep(1)
        
asyncio.create_task(task())
