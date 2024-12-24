import asyncio
import os

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import (API_HASH, API_ID, AUTO_SAVE_CHANNEL_ID, SUDO_USERS,
                    USELESS_IMAGE, WARN_IMAGE)
from Database.count_2 import incr_count_2
from Database.pending_request_db import delete_all
from Database.privileges import get_privileges
from Database.sessions import get_session
from Database.settings import get_settings
from main import app as paa
from Plugins.delete_after import task_initiator
from templates import AUTO_DELETE_TEXT, USELESS_MESSAGE

from . import AUTO_DELETE_STR, tryer
from .start import start_markup as build


async def stop(c: Client):
    try:
        await c.stop()
    except ConnectionError:
        pass

TEMPL = '''┏━━━━━𓆩𝘌𝘳𝘳𝘰𝘳 𝘍𝘰𝘶𝘯𝘥𓆪ꪾ━━━━━┓
♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 : {}

≼𝗪𝗔𝗥𝗡𝗜𝗡𝗚 𝗔𝗟𝗘𝗥𝗧≽
➤**You are Not eligible To Save BOT 
Content ....

➤If You Try To Save Again, Your 
Membership Will Be Dead...**
┗━━━━━━𓆩𝘛𝘦𝘳𝘢𝘉𝘰𝘹𓆪ꪾ━━━━━━┛'''

markup = IKM([[IKB('𝘚𝘩𝘢𝘳𝘦 𝘞𝘪𝘵𝘩 𝘔𝘦', callback_data='sharewithme')]])
global_app = {}
me = None
bots = {}

async def save(C: Client, M: Message):
    if not M.chat.id in bots:
        bots[M.chat.id] = (await tryer(C.get_users, M.chat.id)).is_bot
    global me
    if not me:
        me = await paa.get_me()
    priv = await get_privileges(M.from_user.id)
    if not priv[2]:
        if M.chat.id == me.id:
            return await paa.send_photo(M.from_user.id, WARN_IMAGE, caption=TEMPL.format(M.from_user.mention))
    dm = not bots[M.chat.id]
    if not priv[3]:
        if dm:
            return await tryer(M.delete)
    try:
        count = int(M.text.split()[1])
    except:
        count = 1
    if count > 20:
        return await M.edit('Limit is 20.')
    if not M.reply_to_message:
        return await M.edit('Reply to a file to save.')
    settings = await get_settings()
    st = M.reply_to_message.id
    en = st + count
    messes = await C.get_messages(M.chat.id, list(range(st, en)))
    count = await incr_count_2()
    cops = []
    uffie = await tryer(paa.send_message, M.from_user.id, 'Under processing...')
    
    for msg in messes:
        await asyncio.sleep(1)  # Added delay to avoid rate limits
        if not msg or msg.empty:
            continue 
        if msg.from_user.id == M.from_user.id:
            continue
        if msg.text:
            await uffie.delete()
            cop = await paa.send_message(M.from_user.id, msg.text, reply_markup=markup)
        else:
            if dm:
                if not msg.caption:
                    msg.caption = '#DM'
                else:
                    msg.caption = '#DM\n ' + msg.caption
            try:
                dl = await msg.download()
                await uffie.delete()
                if msg.document:
                    cop = await paa.send_document(M.from_user.id, dl, caption=msg.caption, reply_markup=markup)
                elif msg.video:
                    cop = await paa.send_video(M.from_user.id, dl, caption=msg.caption, reply_markup=markup)
                elif msg.photo:
                    cop = await paa.send_photo(M.from_user.id, dl, caption=msg.caption, reply_markup=markup)
                elif msg.animation:
                    cop = await paa.send_animation(M.from_user.id, dl, caption=msg.caption, reply_markup=markup)
                try:
                    os.remove('downloads/' + dl.split('/')[-1])
                except FileNotFoundError:
                    pass
            except:
                pass
        if settings['auto_save']:
            await cop.copy(AUTO_SAVE_CHANNEL_ID, reply_markup=None)
        cops.append(cop)
    ok = await paa.send_message(M.from_user.id, AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
    await task_initiator(cops, None, ok, count)

@Client.on_message(filters.command('bot'))
async def bot(_, m):
    id = m.from_user.id
    priv = await get_privileges(id)
    if not priv[1]:
        return await tryer(m.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(_, True))
    session = await get_session(id)
    if not session:
        return await m.reply("**Before Use.You Have to Connect with Bot.For Connect Use: /connect **")
    try:
        app = Client(str(id), api_id=API_ID, api_hash=API_HASH, session_string=session)
        await app.start()
        global_app[id] = app
        await m.reply('**UBot Activated\nUse  `..`  To Save Other Bot Content Or User DM Content.**')
        app.add_handler(MessageHandler(save, (filters.command('.', '.') & filters.me)))
        await asyncio.sleep(300)
        try:
            await app.stop()
            await tryer(m.reply, '**UBot Deactivate..**')
        except ConnectionError:
            pass
    except FloodWait as e:
        await asyncio.sleep(e.value)  # Handle FloodWait delay
        return await m.reply(f'Try Again After {e.value} seconds.')
    except:
        return await m.reply('Session Expired.')
    
@Client.on_message(filters.command('resetr') & filters.user(SUDO_USERS))
async def reset_join_req_db(_, m: Message):
    to_edit = await m.reply_text("Deleting all the pending join request from my db")
    total = await delete_all()
    if not total:
        await to_edit.edit_text("No collection found to delete from database")
    else:
        await to_edit.edit_text(f"Deleted data of {total} users from db")
    return

# async def task():
#     while True:
#         x = await get_all_2()
#         for y in x:
#             await asyncio.sleep(1)  # Delay per item processing
#             lis = await get_2(y)
#             if not lis:
#                 continue
#             if int(time.time()-lis[3]) < AUTO_DELETE_TIME:
#                 continue
#             await tryer(paa.delete_messages, y, lis[0])
#             try:
#                 await tryer(paa.edit_message_text, y, lis[1], POST_DELETE_TEXT.format(lis[2]))
#             except:
#                 pass
#             await update_2(y, [])
#         await asyncio.sleep(10)  # Delay for next task cycle

# asyncio.create_task(task())
#No longer needed alreaedy handled in delate after
