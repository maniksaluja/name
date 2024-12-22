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
    print(data)
    
    # Handle 'sharewithme' callback
    if data == 'sharewithme':
        settings = await get_settings()
        await q.answer('Thank You', show_alert=True)
        new_msg = await q.edit_message_reply_markup(reply_markup=None)
        if not settings['auto_save']:
            await new_msg.copy(AUTO_SAVE_CHANNEL_ID)
        return

    if data == "send_voicenote":
        kb = IKM([[IKB("Contact to Buy Now", url=BUY_LINK)]])
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
            await q.edit_message_text("Please wait for a while", reply_markup=None)
        else:
            await q.edit_message_caption("Please wait for a while", reply_markup=None)
        await q.message.reply_audio(FEEDBACK_VOICE, caption="You can take upto 5 minutes to send me a feedback\nAlso note that no commands will work in this duration you can sned /cancel to stop giving feedback")
        USER_LISTENING[user_id] = {}
        current_listening.append(user_id)
        await q.message.delete()
        return

    if data.startswith("feedback_"):
        to_do: str = data.split("_")[1]
        reply_to: Message = q.message.reply_to_message
        if to_do== "approve":
            await q.edit_message_text("Successfully forwarded message to final destination", reply_markup=None)
            if not reply_to:
                await q.answer("Looks like someone have deleted the message I was replying to. I can't proceed further")
                return

            if reply_to.media_group_id:
                await c.forward_media_group(AFTER_FEEDBACK, FEEDBACK_CHANNEL, reply_to.id, hide_sender_name=True)
            else:
                await reply_to.forward(AFTER_FEEDBACK, hide_sender_name=True)
            return

        elif to_do == "reject":
            await q.edit_message_text("Asked owner if he want to give comment to the user or not", reply_markup=None)
            kb = IKM([[IKB("Comment", f"feedback_r:{reply_to.forward_from.id}"), IKB("Ignore", f"feedback_i:{reply_to.forward_from.id}")]])

            await c.send_message(OWNER_ID, f"Do you want to say something to user who have given [this feedback]({reply_to.link})?", disable_web_page_preview=True, reply_markup=kb)
            ADMIN_REPLY_BACK[reply_to.forward_from.id] = {}

            return

        elif to_do.startswith("r:"):
            if Plugins.LISTENING_FOR:
                await q.message.reply_text(f"You are currently replying to [this user](tg://user?id={Plugins.LISTENING_FOR})")
                return
            if Plugins.LISTENING_FOR not in ADMIN_REPLY_BACK:
                await q.edit_message_text("Time's up dude you can't reply to this user anymore", reply_markup=None)
                Plugins.LISTENING_FOR = None

            u_id: int = int(to_do.split(":")[-1])
            Plugins.LISTENING_FOR = u_id
            ADMIN_REPLY_BACK[Plugins.LISTENING_FOR] = {}
            await q.message.reply_text("What do you want to reply to user give me something.\nNote that any command from you will not work right now if u don't want to reply anymore just send /cancel")
            try:
                await q.edit_message_reply_markup(None)
            except MessageNotModified:
                pass
            return
        elif to_do.startswith("i:"):
            await q.edit_message_text("Understand", reply_markup=None)
            u_id: int = int(to_do.split(":")[-1])
            try:
                ADMIN_REPLY_BACK.pop(u_id)
            except:
                pass
            Plugins.LISTENING_FOR = None
            return


    if data == "confirm_send":
        await q.edit_message_text("Thanks for your precious feedback", reply_markup=None)
        func = USER_LISTENING[user_id]["forward"]
        z: Message = await func(FEEDBACK_CHANNEL, q.from_user.id, USER_LISTENING[user_id]["msg_id"])
        kb = IKM([[IKB("Approve", "feedback_approve"), IKB("Reject", "feedback_reject")]])
        if isinstance(z, list):
            z = z[0]
        await z.reply_text(f"Feedback given by: {USER_LISTENING[user_id]['mention']}", reply_markup=kb)
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
            await q.edit_message_text("Bot is no longer listening to you", reply_markup=None)
            return
        await q.edit_message_text("Sent the reply successfully", reply_markup=None)
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
        await q.edit_message_text("Bot is no longer listening to you", reply_markup=None)
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
        'toggle_fwd': 'forwarding'
    }

    if data in toggle_actions:
        setting_key = toggle_actions[data]
        settings, mark = await toggle_setting(setting_key)
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=mark)

    # Handle 'activate' and 'toggle' prefixes (paid-related actions)
    elif data.startswith(("toggleab", "togglesu", "togglemc", "togglead", "activate")):
        await pay_cbq(c, q)
