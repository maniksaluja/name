from pyrogram import Client
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

import Plugins

from . import (ADMIN_REPLY_BACK, USER_LISTENING, current_listening, my_listner,
               my_owner_listner)

media_groupp = {} #{userid: mediagrpid}


async def is_media_group(m: Message):
    global media_groupp
    if not m.from_user:
        return False
    return bool(media_groupp.get(m.from_user.id, None))

@Client.on_message(my_owner_listner, -106)
async def _listen_to_owner_(c: Client, m: Message):
    global ADMIN_REPLY_BACK
    global media_groupp

    if m.text == "/start":
        await m.reply_text("**Request Terminated By You**")
        try:
            ADMIN_REPLY_BACK.pop(Plugins.LISTENING_FOR)
        except:
            pass
        
        Plugins.LISTENING_FOR = None
        return

    kb = IKM([
        [
            IKB("𝘚𝘦𝘯𝘥", f"send_r:{Plugins.LISTENING_FOR}")
        ],
        [
            IKB("𝘊𝘢𝘯𝘤𝘦𝘭", f"send_i:{Plugins.LISTENING_FOR}")
        ]
    ])

    txt = "Are you sure you want to send it as reply??"

    if media_groupp.get(m.from_user.id, None):
        return
    if m.media and m.media_group_id:
        func = c.forward_media_group
        media_groupp[m.from_user.id] = m.media_group_id
    else:
        func = c.forward_messages

    ADMIN_REPLY_BACK[Plugins.LISTENING_FOR] = {"forward": func, "to_user": Plugins.LISTENING_FOR, "msg_id": m.id}

    await m.reply_text(txt, reply_markup=kb)
    m.stop_propagation()
    return

@Client.on_message(my_listner, -18)
async def _listner_(c: Client, m: Message):
    global USER_LISTENING
    global media_groupp
    global current_listening

    if m.text == "/start":
        await m.reply_text(" **Request Terminated By You** ")
      
        try:
            USER_LISTENING.pop(m.from_user.id)
        except:
            pass
        try:
            current_listening.pop(m.from_user.id)
        except:
            pass
        return

    kb = IKM(
        [
            [
                IKB("𝘠𝘦𝘴 𝘐 𝘈𝘮 𝘚𝘶𝘳𝘦", f"confirm_send")
            ],
            [
                IKB("𝘕𝘰 𝘐 𝘈𝘮 𝘕𝘰𝘵", "don_t_send")
            ]
        ]
    )

    txt = "**Are You Sure this is your Request ??**"

    if media_groupp.get(m.from_user.id, None):
        return
    if m.media and m.media_group_id:
        func = c.forward_media_group
        media_groupp[m.from_user.id] = m.media_group_id
    else:
        func = c.forward_messages

    username = m.from_user.mention
    USER_LISTENING[m.from_user.id] = {"forward": func, "mention": username, "msg_id": m.id}
    await m.reply_text(txt, reply_markup=kb)
    try:
        current_listening.remove(m.from_user.id)
    except:
        pass
    m.stop_propagation()
    return
