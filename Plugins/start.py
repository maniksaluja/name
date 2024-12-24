import asyncio
from typing import List

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message, User

from config import (AUTO_DELETE_TIME, CONTENT_SAVER, DB_CHANNEL_2_ID,
                    DB_CHANNEL_ID, FSUB_1, FSUB_2, RFSUB, STICKER_ID,
                    TUTORIAL_LINK)
from Database.encr import get_encr
from Database.pending_request_db import is_user_pending
from Database.privileges import get_privileges
from Database.settings import get_settings
from Database.users import add_user, is_user
from main import app
from templates import (AUTO_DELETE_TEXT, CUSTOM_CAPTION, FILE_PATH,
                       START_MESSAGE, START_MESSAGE_2, TRY_AGAIN_TEXT)

from . import AUTO_DELETE_STR, tryer
from .block import block_dec
from .delete_after import get_cur_ep, task_initiator
from .encode_decode import Char2Int, decrypt

members = {FSUB_1: [], FSUB_2: []} # {chat_id: [user_id]}

FSUB = [FSUB_1, FSUB_2]
if RFSUB and RFSUB[0]:
    for i in RFSUB:
        if i not in FSUB:
            FSUB.append(i)
        if i not in members:
            members[i] = []


@Client.on_message(filters.chat(FSUB) & (filters.new_chat_members | filters.left_chat_member))
async def cmufunc(_, m: Message):
    if m.new_chat_members:
        users: List[User] = m.new_chat_members
        for user in users:
            members[m.chat.id].append(user.id)
    elif m.left_chat_member:
        try:
            members[m.chat.id].remove(m.left_chat_member.id)
        except:
            pass
        
async def check_fsub(user_id: int) -> bool:
    for y in FSUB:
        y = int(y)
        try:
            x = await app.get_chat_member(y, user_id)
            if not (x.status in [CMS.OWNER, CMS.ADMINISTRATOR, CMS.MEMBER]):
                return False
        except:
            if await is_user_pending(user_id, y):
                continue
            return False
        
    return True

me = None
chats = {}

async def get_chats(c: Client):
    global chats
    if not chats:
        for x in FSUB:
            crt = False
            r = x
            if x in RFSUB or x == FSUB_1:
                crt = True
                r = x
            try:
                y = await c.create_chat_invite_link(x, creates_join_request=crt)
                chats[x] = y.invite_link
            except:
                continue
    
    return chats

async def markup(_, link=None) -> IKM:
    global chats
    if not chats:
        chats = await get_chats(_)
    mark = []
    
    for id_, chat in chats.items():
        if id_ in RFSUB or id_ == FSUB_1:
            mark.append([IKB("Send join request", url=chat)])
        else:
            mark.append([IKB("Join channel", url=chat)])
    
    mark.append([IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)])
    if link:
        mark.append([IKB('ᴛʀʏ ᴀɢᴀɪɴ♻️', url=link)])
    
    markup = IKM(mark)
    return markup

async def start_markup(_, feedback_req = False, tbelow = False) -> IKM:
    global chats
    if not chats:
        chats = await get_chats(_)
    
    if not tbelow:
        mark = [[IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)], [IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[FSUB_1]), IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[FSUB_2])]]
    else:
        mark = [[IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[FSUB_1]), IKB('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url=chats[FSUB_2])], [IKB("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴇʀᴀʙᴏx ʙᴏᴛ", url=TUTORIAL_LINK)]]
    if feedback_req:
        mark.append([IKB("sᴇɴᴅ ʀᴇϙᴜᴇsᴛ ", "give_feedback")])
    markup = IKM(mark)
    return markup

control_batch = []

@block_dec
async def start(_: Client, m: Message):
    global me
    is_enabled_voice = (await get_settings()).get('download', True)
    if FILE_PATH and is_enabled_voice:
        voice_n_kb = IKM(
            [
                [
                    IKB("ᴅᴏᴡɴʟᴏᴀᴅ ", "send_voicenote")
                ]
            ]
        )
    else:
        voice_n_kb = None
    if not me:
        me = await _.get_me()
    print(m.text)
    user_id = m.from_user.id
    if not await is_user(user_id):
        await add_user(user_id)
        return await m.reply(START_MESSAGE.format(m.from_user.mention), reply_markup=await start_markup(_, tbelow=True))
    if CONTENT_SAVER:
        prem = (await get_privileges(user_id))[2]
    else:
        prem = True
    
    txt = m.text.split()
    okkie = None
    if len(txt) > 1:
        command = txt[1]
        if command.startswith('get'):
            encr = command[3:]
            if not await check_fsub(user_id):
                mark = await markup(_, f'https://t.me/{me.username}?start=get{encr}')
                await m.reply(TRY_AGAIN_TEXT.format(m.from_user.mention), reply_markup=mark)
                return 
            std = await m.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')
            try:
                msg = await _.get_messages(DB_CHANNEL_ID, Char2Int(spl[0]))
                if msg.empty:
                    msg = await _.get_messages(DB_CHANNEL_2_ID, Char2Int(spl[2]))
            except:
                msg = await _.get_messages(DB_CHANNEL_2_ID, Char2Int(spl[2]))
            await std.delete()
            cap = CUSTOM_CAPTION
            if CAP:=msg.caption:
                ep = get_cur_ep(CAP)
                if ep:
                    cap = f"{CUSTOM_CAPTION}\n{ep}"
            if not prem:
                
                ok = await tryer(msg.copy, user_id, caption=cap, reply_markup=voice_n_kb, protect_content=True)
            else:
                ok = await tryer(msg.copy, user_id, caption=cap, reply_markup=voice_n_kb)
            if AUTO_DELETE_TIME:
                ok1 = await ok.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                haha = [ok]
                await task_initiator(haha, f'https://t.me/{me.username}?start=get{encr}', ok1)
            return
        elif command.startswith('batchone'):
            encr = command[8:]
            link = f'https://t.me/{me.username}?start=batchone{encr}'
            if not await check_fsub(user_id):
                mark = await markup(_, link)
                await m.reply(TRY_AGAIN_TEXT.format(m.from_user.mention), reply_markup=mark)
                return 
            std = await m.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')[0].split('-')
            st = Char2Int(spl[0])
            en = Char2Int(spl[1])
            if st == en:
                messes = [await _.get_messages(DB_CHANNEL_ID, st)]
            else:
                mess_ids = []
                while en - st + 1 > 200:
                    mess_ids.append(list(range(st, st + 200)))
                    st += 200
                if en - st + 1 > 0:
                    mess_ids.append(list(range(st, en+1)))
                messes = []
                for x in mess_ids:
                    messes += (await _.get_messages(DB_CHANNEL_ID, x))
            if not messes:
                new_encr = await get_encr(encr)
                if new_encr:
                    spl = decrypt(new_encr).split('|')[0].split('-')
                    st = Char2Int(spl[0])
                    en = Char2Int(spl[1])
                    if st == en:
                        messes = [await _.get_messages(DB_CHANNEL_2_ID, st)]
                    else:
                        mess_ids = []
                        while en - st + 1 > 200:
                            mess_ids.append(list(range(st, st + 200)))
                            st += 200
                        if en - st + 1 > 0:
                            mess_ids.append(list(range(st, en+1)))
                        messes = []
                        for x in mess_ids:
                            messes += (await _.get_messages(DB_CHANNEL_2_ID, x))
            if len(messes) > 10:
                okkie = await m.reply("**It's Take Few Seconds...**")
            haha = []
            if not prem:
                for x in messes:
                    if not x:
                        continue
                    if x.empty:
                        continue
                    cap = CUSTOM_CAPTION
                    if CAP:=x.caption:
                        ep = get_cur_ep(CAP)
                        if ep:
                            cap = f"{CUSTOM_CAPTION}\n{ep}"
                    
                    gg = await tryer(x.copy, user_id, caption=cap, reply_markup=voice_n_kb, protect_content=True)
                    haha.append(gg)
                    await asyncio.sleep(1)
            else:
                for x in messes:
                    if not x:
                        continue
                    if x.empty:
                        continue
                    cap = CUSTOM_CAPTION
                    if CAP:=x.caption:
                        ep = get_cur_ep(CAP)
                        if ep:
                            cap = f"{CUSTOM_CAPTION}\n{ep}"
                    
                    gg = await tryer(x.copy, user_id, caption=cap, reply_markup=voice_n_kb)
                    haha.append(gg)
                    await asyncio.sleep(1)
                    # tasks.append(asyncio.create_task(x.copy(user_id)))
            await std.delete()
            if AUTO_DELETE_TIME:
                ok1 = await m.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                if haha:
                    await task_initiator(haha, link, ok1)
            if okkie:
                await okkie.delete()
            return
        elif command.startswith('batchtwo'):
            encr = command[8:]
            link = f'https://t.me/{me.username}?start=batchtwo{encr}'
            if not await check_fsub(user_id):
                mark = await markup(_, link)
                return await m.reply(TRY_AGAIN_TEXT.format(m.from_user.mention), reply_markup=mark)
            std = await m.reply_sticker(STICKER_ID)
            spl = decrypt(encr).split('|')[0].split('-')
            st = Char2Int(spl[0])
            en = Char2Int(spl[1])
            if st == en:
                messes = [await _.get_messages(DB_CHANNEL_2_ID, st)]
            else:
                mess_ids = []
                while en - st + 1 > 200:
                    mess_ids.append(list(range(st, st + 200)))
                    st += 200
                if en - st + 1 > 0:
                    mess_ids.append(list(range(st, en+1)))
                messes = []
                for x in mess_ids:
                    messes += (await _.get_messages(DB_CHANNEL_2_ID, x))
            okkie = None
            if len(messes) > 10:
                okkie = await m.reply("**It's Take Few Seconds....**")
            haha = []
            if not prem:
                for x in messes:
                    if not x:
                        continue
                    if x.empty:
                        continue
                    cap = CUSTOM_CAPTION
                    if CAP:=x.caption:
                        ep = get_cur_ep(CAP)
                        if ep:
                            cap = f"{CUSTOM_CAPTION}\n{ep}"
                    
                    gg = await tryer(x.copy, user_id, caption=cap, reply_markup=voice_n_kb, protect_content=True)
                    haha.append(gg)
                    await asyncio.sleep(1)
            else:
                for x in messes:
                    if not x:
                        continue
                    if x.empty:
                        continue
                    cap = CUSTOM_CAPTION
                    if CAP:=x.caption:
                        ep = get_cur_ep(CAP)
                        if ep:
                            cap = f"{CUSTOM_CAPTION}\n{ep}"
                    gg = await tryer(x.copy, user_id, caption=cap, reply_markup=voice_n_kb)
                    haha.append(gg)
                    await asyncio.sleep(1)
            await std.delete()
            if AUTO_DELETE_TIME:
                ok1 = await m.reply(AUTO_DELETE_TEXT.format(AUTO_DELETE_STR))
                await task_initiator(haha, link, ok1)
            if okkie:
                await okkie.delete()
            return
    else:
        await m.reply_text(START_MESSAGE_2.format(m.from_user.mention), reply_markup=await start_markup(_, tbelow=True))
        

@Client.on_message(filters.command('start') & filters.private)
async def start_func(_, m: Message):
    user_id = m.from_user.id
    if user_id in control_batch:
        return
    control_batch.append(user_id)

    try:
        await start(_, m)
    except:
        pass

    control_batch.remove(user_id) if user_id in control_batch else None
