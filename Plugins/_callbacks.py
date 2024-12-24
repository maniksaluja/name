import time
from pyrogram import Client, raw
from pyrogram.errors.exceptions import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM, Message
from config import (
    AFTER_FEEDBACK, AUTO_SAVE_CHANNEL_ID, BUY_LINK, FEEDBACK_CHANNEL,
    OWNER_ID, SUDO_USERS
)
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
    global USER_LISTENING, current_listening, ADMIN_REPLY_BACK

    # Function for toggling settings
    async def toggle_setting(setting_key, default_value=False):
        settings = await get_settings()
        if "forwarding" not in settings:
            settings["forwarding"] = True

        if setting_key == "logs":
            toggle_able = ["both", "l1", "l2", False]
            index = (toggle_able.index(settings["logs"]) + 1) if toggle_able.index(settings["logs"]) != len(toggle_able) - 1 else 0
            settings["logs"] = toggle_able[index]
        elif setting_key == "generate":
            cur = int(settings.get(setting_key, 10))
            settings[setting_key] = 10 if cur == 1 else 1
        else:
            settings[setting_key] = not settings.get(setting_key, default_value)

        await update_settings(settings)
        markup_content = markup(settings)
        return settings, markup_content

    # Handle callbacks
    if data == "sharewithme":
        settings = await get_settings()
        await q.answer("Thank You", show_alert=True)
        new_msg = await q.edit_message_reply_markup(reply_markup=None)
        if not settings["auto_save"]:
            await new_msg.copy(AUTO_SAVE_CHANNEL_ID)
        return

    if data == "send_voicenote":
        kb = IKM([[IKB("𝘉𝘶𝘺 𝘕𝘰𝘸", url=BUY_LINK)]])
        try:
            await q.message.reply_audio(
                FILE_PATH,
                caption="> **UNLOCK UNLIMITED Downloads for just ₹79!**",
                reply_markup=kb
            )
            await q.edit_message_reply_markup(None)
        except MessageIdInvalid as e:
            print(f"MessageIdInvalid Error in 'send_voicenote': {e}")
        except MessageNotModified as e:
            print(f"MessageNotModified Error in 'send_voicenote': {e}")
        except Exception as e:
            print(f"Error in 'send_voicenote': {e}")
        return

    if data == "give_feedback":
        text = q.message.text or q.message.caption
        await q.edit_message_text("**Generating Request...**", reply_markup=None)
        await q.message.reply_audio(
            FEEDBACK_VOICE,
            caption="**Share your feedback below. Once done, click 'Sure' to send it to the admin.**"
        )
        USER_LISTENING[user_id] = {}
        current_listening.append(user_id)
        await q.message.delete()
        return

    if data.startswith("feedback_"):
        action = data.split("_")[1]
        reply_to = q.message.reply_to_message
        if action == "approve":
            await q.edit_message_text("**Request Uploaded Successfully!**", reply_markup=None)
            if reply_to:
                kb = IKM([[IKB("Talk to Admin", url="https://t.me/CuteGirlTG")]])
                await reply_to.copy(AFTER_FEEDBACK, reply_markup=kb)
            else:
                await q.answer("Message not found.")
            return
        elif action == "reject":
            await q.edit_message_text("**Request Rejected.**", reply_markup=None)
            kb = IKM([
                [IKB("YES", f"feedback_r:{reply_to.forward_from.id}"),
                 IKB("NO", f"feedback_i:{reply_to.forward_from.id}")]
            ])
            try:
                await c.send_message(
                    OWNER_ID,
                    f"**Do you want to add a note for this [request]({reply_to.link})?**",
                    disable_web_page_preview=True,
                    reply_markup=kb
                )
            except MessageNotModified as e:
                print(f"MessageNotModified Error in 'reject feedback': {e}")
            ADMIN_REPLY_BACK[reply_to.forward_from.id] = {}
            return

    if data.startswith("info_"):
        info_abt = data.split("_")[1]
        start = time.perf_counter()
        await c.invoke(raw.functions.Ping(ping_id=c.rnd_id()))
        ping = (time.perf_counter() - start) * 1000
        info, kb = get_system_info(info_abt)
        txt = f"**Ping: {ping} ms**\n**Info about {info_abt}:**\n"
        for key, value in info.items():
            txt += f"• {key}: `{value}`\n"
        if info_abt == "network":
            download, upload = current_speed()
            txt += f"{download}\n{upload}"
        try:
            await q.edit_message_text(txt, reply_markup=kb)
        except MessageNotModified as e:
            print(f"MessageNotModified Error in 'info_': {e}")
        return

    if data.startswith("toggle"):
        setting_key = data.split("_")[1]
        settings, mark = await toggle_setting(setting_key)
        await q.answer("Updating values...")
        # Check if the current reply_markup is the same as the new one
        try:
            if q.message.reply_markup != mark:
                await q.edit_message_reply_markup(reply_markup=mark)
            else:
                print("No changes in markup, skipping edit.")
        except MessageNotModified as e:
            print(f"MessageNotModified Error in 'toggle': {e}")
