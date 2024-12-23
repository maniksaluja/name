import time

from pyrogram import Client, raw
from pyrogram.errors.exceptions import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

import Plugins
from config import (AFTER_FEEDBACK, AUTO_SAVE_CHANNEL_ID, BUY_LINK,
                    FEEDBACK_CHANNEL, OWNER_ID, SUDO_USERS)
from Database.settings import get_settings, update_settings
from templates import FEEDBACK_VOICE, FILE_PATH

from . import ADMIN_REPLY_BACK, USER_LISTENING, current_listening, listner
from .paid import pay_cbq
from .settings import markup
from .system_info import current_speed, get_system_info


@Client.on_callback_query()
async def cbq(c: Client, q: CallbackQuery):
    data = q.data
    user_id = q.from_user.id
    global USER_LISTENING
    global current_listening
    global ADMIN_REPLY_BACK
    
    # Handle 'sharewithme' callback
    if data == 'sharewithme':
        settings = await get_settings()
        await q.answer('Thank You', show_alert=True)
        new_msg = await q.edit_message_reply_markup(reply_markup=None)
        if not settings['auto_save']:
            await new_msg.copy(AUTO_SAVE_CHANNEL_ID)
        return

    if data == "send_voicenote":
        kb = IKM([[IKB("𝘉𝘶𝘺 𝘕𝘰𝘸", url=BUY_LINK)]])
        try:
            await q.message.reply_audio(FILE_PATH, reply_markup=kb)
        except MessageIdInvalid:
            pass
        except Exception as e:
            print(f"Error at line send_voienote: {e}")
        try:
            await q.edit_message_reply_markup(None)
        except MessageIdInvalid:
            pass
        except Exception as e:
            print(f"Error at line send_voienote: {e}")
        return

    if data == "give_feedback":
        if q.message.text:
            await q.edit_message_text("**Generating Request....**", reply_markup=None)
        else:
            await q.edit_message_caption("**Generating Request......**", reply_markup=None)
        await q.message.reply_audio(FEEDBACK_VOICE, caption="**• Share your content or content request below \n • Mention any issues, suggestions, or queries \n• Once you're done, click 'Sure' to forward your message directly to the admin for review \n\nTHANK YOU ✨**")
        USER_LISTENING[user_id] = {}
        current_listening.append(user_id)
        await q.message.delete()
        return

    if data.startswith("feedback_"):
        to_do: str = data.split("_")[1]
        reply_to: Message = q.message.reply_to_message
        if to_do== "approve":
            await q.edit_message_text("**This Request Successfully Uploaded On Share&Care**", reply_markup=None)
            if not reply_to:
                await q.answer("Looks like someone have deleted the message I was replying to. I can't proceed further")
                return
            kb = IKM([[IKB("𝘵𝘢𝘭𝘬 𝘛𝘰 𝘈𝘥𝘮𝘪𝘯", url="https://t.me/CuteGirlTG")]])
            if reply_to.media_group_id:
                x = await c.forward_media_group(AFTER_FEEDBACK, FEEDBACK_CHANNEL, reply_to.id, hide_sender_name=True,)
                await x[0].reply_text(" **New Request**", reply_markup=kb)
            else:
                await reply_to.copy(AFTER_FEEDBACK, reply_markup=kb)
            
            return

        elif to_do == "reject":
            await q.edit_message_text("**REQUEST REJECTED \n > Check Your Inbox I sended You Msg Related This Request** ", reply_markup=None)
            kb = IKM([[IKB("𝘠𝘌𝘚", f"feedback_r:{reply_to.forward_from.id}"), IKB("𝘕𝘖", f"feedback_i:{reply_to.forward_from.id}")]])

            await c.send_message(OWNER_ID, f"**Do You Want To Say Something About This [Request]**({reply_to.link})?", disable_web_page_preview=True, reply_markup=kb)
            ADMIN_REPLY_BACK[reply_to.forward_from.id] = {}

            return

        elif to_do.startswith("r:"):
            if Plugins.LISTENING_FOR:
                await q.message.reply_text(f"**Okey Now You Can Type Note For** [this user](tg://user?id={Plugins.LISTENING_FOR})")
                return
            if Plugins.LISTENING_FOR not in ADMIN_REPLY_BACK:
                await q.edit_message_text("Time's UP", reply_markup=None)
                Plugins.LISTENING_FOR = None

            u_id: int = int(to_do.split(":")[-1])
            Plugins.LISTENING_FOR = u_id
            ADMIN_REPLY_BACK[Plugins.LISTENING_FOR] = {}
            await q.message.reply_text("**Okay Now You Can Type Your Message' If You Want to Stop This Proses Use** /cancel")
            try:
                await q.edit_message_reply_markup(None)
            except MessageNotModified:
                pass
            return
        elif to_do.startswith("i:"):
            await q.edit_message_text("**Okey Request Rejected**", reply_markup=None)
            u_id: int = int(to_do.split(":")[-1])
            try:
                ADMIN_REPLY_BACK.pop(u_id)
            except:
                pass
            Plugins.LISTENING_FOR = None
            return


    if data == "confirm_send":
        await q.edit_message_text("**Your Request Successfully Sended to TEAM**", reply_markup=None)
        func = USER_LISTENING[user_id]["forward"]
        z: Message = await func(FEEDBACK_CHANNEL, q.from_user.id, USER_LISTENING[user_id]["msg_id"])
        kb = IKM([[IKB("𝘜𝘱𝘭𝘰𝘢𝘥", "feedback_approve"), IKB("𝘙𝘦𝘫𝘦𝘤𝘵 ", "feedback_reject")]])
        if isinstance(z, list):
            z = z[0]
        await z.reply_text(f"**Request given by:** {USER_LISTENING[user_id]['mention']}", reply_markup=kb)
        try:
            USER_LISTENING.pop(user_id)
        except:
            pass
        try:
            listner.media_groupp.pop(user_id)
        except:
            pass
        return

    if data.startswith("send_r:") or data.startswith("send_i:"):
        to_id = int(data.split(":")[-1])
        if data.split(":")[0] == "send_i":
            try:
                ADMIN_REPLY_BACK.pop(to_id)
            except:
                pass
            try:
                listner.media_groupp.pop(user_id)
            except:
                pass
            
            Plugins.LISTENING_FOR = None
            await q.edit_message_text("**Request terminated**", reply_markup=None)
            return
        await q.edit_message_text("**Reply Successfully Sended**", reply_markup=None)
        func = ADMIN_REPLY_BACK[to_id]["forward"]
        await func(to_id, user_id, ADMIN_REPLY_BACK[to_id]["msg_id"], hide_sender_name=True)
        try:
            ADMIN_REPLY_BACK.pop(to_id)
        except:
            pass
        try:
            listner.media_groupp.pop(user_id)
        except:
            pass
        
        return

    if data == "don_t_send":
        await q.edit_message_text("**Your Request Terminated By You**", reply_markup=None)
        try:
            USER_LISTENING.pop(user_id)
        except:
            pass
        try:
            listner.media_groupp.pop(user_id)
        except:
            pass
        
        return

    if data.startswith("info_"):
        info_abt = data.split("_")[1]
        rnd = c.rnd_id()

        start = time.perf_counter()
        await c.invoke(raw.functions.Ping(ping_id=rnd))
        ping = (time.perf_counter()-start) * 1000
        


        info, kb = get_system_info(info_abt)
        txt = f"**Current Ping: {ping}**\n**Info about {info_abt}:**\n"
            
        for key, value in info.items():
            txt += f"• {key}: `{value}`\n"
        if info_abt == "network":
            download, upload = current_speed()
            txt += f"{download}\n"
            txt += upload
        await q.edit_message_text(txt, reply_markup=kb)
        return
        
    # Handle 'connect' callback
    if data == 'connect':
        await q.answer()
        return await q.message.reply('Type /connect.')

    # Restrict access to sudo users
    if user_id not in SUDO_USERS:
        return await q.answer()

    # Define helper function for toggling settings
    async def toggle_setting(setting_key, default_value=False):
        settings = await get_settings()
        if 'forwarding' not in settings:
            settings['forwarding'] =True
            
        if setting_key == "logs":
            toggle_able = ["both", "l1", "l2", False]
            index = (toggle_able.index(settings["logs"]) + 1) if toggle_able.index(settings["logs"]) != len(toggle_able)-1 else 0
            settings["logs"] = toggle_able[index]
        elif setting_key == "generate":
            cur = int(settings.get(setting_key, 10))
            next_ = 10 if cur == 1 else 1
            settings[setting_key] = next_
        else:
            settings[setting_key] = not settings.get(setting_key, default_value)
        await update_settings(settings)
        markup_content = markup(settings)
        return settings, markup_content

    # Handle toggling various settings
    toggle_actions = {
        'toggle_approval': 'auto_approval',
        'toggle_join': 'join',
        'toggle_leave': 'leave',
        'toggle_image': 'image',
        'toggle_gen': 'generate',
        'toggle_save': 'auto_save',
        'toggle_logs': 'logs',
        'toggle_fwd': 'forwarding',
        'toggle_dl': 'download'
    }

    if data in toggle_actions:
        setting_key = toggle_actions[data]
        settings, mark = await toggle_setting(setting_key)
        await q.answer("Updating values...")
        await q.edit_message_reply_markup(reply_markup=mark)

    # Handle 'activate' and 'toggle' prefixes (paid-related actions)
    elif data.startswith(("toggleab", "togglesu", "togglemc", "togglead", "activate")):
        await pay_cbq(c, q)
