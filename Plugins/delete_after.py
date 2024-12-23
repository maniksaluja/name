import asyncio
from re import findall
from typing import List

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import AUTO_DELETE_TIME
from Database.count import get_count
from templates import POST_DELETE_TEXT

from .encode_decode import Char2Int, decrypt


def get_cur_ep(txt: str, has_req: bool = True):
    if matches := findall(r"#EP\d+", txt):
        if not has_req:
            return matches[-1].replace("#EP","").strip()
        return matches[-1]
    else:
        return 0


async def Delete_task(m: List[Message], link: str or None=None, to_edit: Message or None = None, count: str or None = None):
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
    if cur:
        cur = count
    elif link:
        if 'get' in link:
            cur = Char2Int(decrypt(link.split('get')[1]).split('|')[1])
        else:
            cur = Char2Int(decrypt(link.split('batch')[1][3:]).split('|')[1])

    else:
        if txt:
            cur = get_cur_ep(txt, False)
    if not cur:
        cur = await get_count()
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Get again", url=link)]])
    if to_edit:
        await to_edit.edit_text(POST_DELETE_TEXT.format(cur), reply_markup=kb)
    return

async def task_initiator(m: List[Message], link=None, to_edit: Message or None = None, count: str or None = None):
    if AUTO_DELETE_TIME:
        asyncio.create_task(Delete_task(m, link, to_edit, count))
    return