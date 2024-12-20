from pyrogram import Client, filters
from pyrogram.errors import (PasswordHashInvalid, PhoneCodeInvalid,
                             PhoneNumberInvalid, SessionPasswordNeeded)
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from config import API_HASH, API_ID, PHONE_NUMBER_IMAGE, USELESS_IMAGE
from Database.privileges import get_privileges
from Database.sessions import *
from templates import USELESS_MESSAGE

from . import tryer
from .start import start_markup as build

phone_markup = IKM([[IKB('𝘚𝘩𝘰𝘳𝘵𝘤𝘶𝘵', url='tg://settings')]])

dic = {}
watch = 69

def in_work(id):
  return id in dic

@Client.on_message(filters.command('connect') & filters.private)
async def conn(_, m):
  id = m.from_user.id
  priv = await get_privileges(id)
  if not priv[1]:
    return await tryer(m.reply_photo, USELESS_IMAGE, caption=USELESS_MESSAGE, reply_markup=await build(_))
  session = await get_session(id)
  if session:
    app = Client(str(id), api_id=API_ID, api_hash=API_HASH, session_string=session)
    try:
      await app.start()
      await m.reply('**You Are Already Connected User**')
      await app.stop()
      return
    except:
      await del_session(id)
  if id in dic:
    return await m.reply("**Process Ongoing..., use /terminate to cancel.**")
  await m.reply_photo(PHONE_NUMBER_IMAGE, caption="**Enter Your Phone Number With Country Code. \n <pre>How To Find Number?</pre> \n You can Use Shortcut Button To Find Your Number ** \n <pre>Incase Shortcut Button Not Wokring Than You Need To Find Manually</pre>", reply_markup=phone_markup)
  cli = Client(str(id), api_id=API_ID, api_hash=API_HASH)
  dic[id] = [cli]
  await cli.connect()
  
@Client.on_message(filters.private, group=watch)
async def cwf(_, m):
  id = m.from_user.id
  if not in_work(id):
    return
  if not m.text:
    return
  if m.text.startswith("/"):
    return
  lis = dic[id]
  if len(lis) == 1:
    cli = lis[0]
    lis.append(m.text)
    try:
      hash = await cli.send_code(m.text)
    except ConnectionError:
      await cli.connect()
      hash = await cli.send_code(m.text)
    except PhoneNumberInvalid:
      dic.pop(id)
      return await m.reply('**Phone Number Is Invalid.**', reply_markup=phone_markup)
    lis.append(hash.phone_code_hash)
    await m.reply("**Enter OTP:**")
    dic[id] = lis
  elif len(lis) == 3:
    cli = lis[0]
    txt = m.text.replace(" ", "") if " " in m.text else m.text
    lis.append(txt)
    dic[id] = lis
    try:
      await cli.sign_in(lis[1], lis[2], lis[3])
      session = await cli.export_session_string()
      await update_session(id, session)
      await cli.disconnect()
      dic.pop(id)
      await m.reply("**Successfully Connected..**")
    except PhoneCodeInvalid:
      dic.pop(id)
      return await m.reply('**Invalid OTP!**')
    except SessionPasswordNeeded:
      await m.reply("**Enter Two Step Verification Password:**")
  elif len(lis) == 4:
    lis.append(m.text)
    cli = lis[0]
    try:
      await cli.check_password(lis[4])
      await cli.sign_in(lis[1], lis[2], lis[3])
    except PhoneCodeInvalid:
      dic.pop(id)
      return await m.reply('**Invalid OTP!**')
    except PasswordHashInvalid:
      dic.pop(id)
      return await m.reply('**Invalid Two Step Verification Password.**')
    session = await cli.export_session_string()
    await update_session(id, session)
    await cli.disconnect()
    dic.pop(id)
    await m.reply("**Connected Successfully.**")
    
@Client.on_message(filters.command("terminate"))
async def term(_, m):
  id = m.from_user.id
  if not in_work(id):
    return
  dic.pop(id)
  await m.reply("**Process Terminated.**")
