import asyncio
from re import findall
from typing import List

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import AUTO_DELETE_TIME
from Database.count import get_count
from templates import POST_DELETE_TEXT


def get_cur_ep(txt: str, has_req: bool = True):
    if matches := findall(r"#EP\d+", txt):
        if not has_req:
            matches[-1].replace("#EP","")
        return matches[-1]
    else:
        return 0


async def Delete_task(m: List[Message], link=None):
    await asyncio.sleep(AUTO_DELETE_TIME)
    z = m[-1]
    for i in m:
        if not i.empty:
            try:
                await i.delete()
            except:
                continue
    txt = z.text if z.text else z.caption
    cur = False
    if txt:
        cur = get_cur_ep(txt, False)
    if not cur:
        cur = await get_count()
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Get again", url=link)]])
    await z.reply_text(POST_DELETE_TEXT.format(cur), reply_markup=kb)
    return

async def task_initiator(m: List[Message], link=None):
    if AUTO_DELETE_TIME:
        asyncio.create_task(Delete_task(m, link))
    return