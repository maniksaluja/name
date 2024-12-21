import os
from pathlib import Path

BASE_DRI = Path(__file__).resolve().parent #Get the parent directory 

filename = "uff.ogg" #File name which you want send when user click on Download button. You can give the wrong name or just set the FILE_PATH to none so the bot will not genrate download button

feedback_voice = "uff.ogg"

FILE_PATH = os.path.join(BASE_DRI, "Voice", filename) #Join the path to the audio file

FEEDBACK_VOICE = os.path.join(BASE_DRI, "Voice", feedback_voice)
if not os.path.exists(FEEDBACK_VOICE):
    FEEDBACK_VOICE = None

if not os.path.exists(FILE_PATH): #Chech if the path exists or not
    FILE_PATH = None #If path is not valid FILE_PATH will be set to None


LINK_GEN = """
┏━━━༺𝘍𝘈𝘕𝘉𝘢𝘴𝘦༻━━━┓
☞ 𝘥𝘦𝘴𝘤𝘳𝘪𝘱𝘵𝘪𝘰𝘯: @Ultra_XYZ


☞ 𝘦𝘱𝘪𝘴𝘰𝘥𝘦 : {} {}
┗━━━༺▾𝖡𝖮𝖳𝘓𝘪𝘯𝘬▾༻━━━┛

{}
"""

USELESS_MESSAGE = "𓆩𝗘𝗥𝗥𝗢𝗥 𝗙𝗢𝗨𝗡𝗗𓆪ꪾ\n<b>𝘗𝘭𝘦𝘢𝘴𝘦 𝘋𝘰𝘯'𝘵 𝘚𝘦𝘯𝘥 𝘜𝘯𝘸𝘢𝘯𝘵𝘦𝘥 𝘔𝘦𝘴𝘴𝘢𝘨𝘦𝘴</b>\n\n♛ 𝙏𝙝𝙖𝙣𝙠𝙔𝙤𝙪 ♛\n𝘾𝙝𝙚𝙘𝙠 𝙊𝙐𝙏 𝙊𝙛𝙛𝙞𝙘𝙞𝙖𝙡 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𖡦"

LEAVE_MESSAGE = "<pre>Hey Why Are You Leaving  ME Please Don't Go I am Useless Without You🥹😢</pre>\n\n\n<pre>If Any Problem then Talk To Me \nBUT don't leave Me 😭💔</pre>\n\n𝗠𝗬 𝗧𝗚 𝗜𝗗 : @CuteGirlTG"

AUTO_DELETE_TEXT = " **•This Will Be AUTO DELETED IN {}\n╼╾╼╾╼╾╼⊰☝🏻⊱╾╼╾╼╾╼╾\n ☛ WHY?~  Due To CopyRights.** "

POST_DELETE_TEXT = """ **EXTREMELY SORRY BUT!!!!!
╼╾╼╾╼╾╼⊰𝘦𝘱 {} ⊱╾╼╾╼╾╼╾
❖MEDIEA SUCCESSFULLY DELETED** """

JOIN_MESSAGE = """♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 : {} 
<b>Your Joining Request IS Accepted 

<pre>𝙄𝙢𝙥𝙤𝙧𝙩𝙖𝙣𝙩 𝙉𝙤𝙩𝙚 : 
If you don't know how to open link than click on tutorial given Below 𖡶</pre>

Welcome To Shanaya FANBase Channel</b>"""

START_MESSAGE_2 = """┏━━━━𓆩𝘌𝘳𝘳𝘰𝘳 𝘍𝘰𝘶𝘯𝘥𓆪ꪾ━━━━┓
♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 : {}

≼𝙀𝙍𝙍𝙊𝙍 𝙁𝙊𝙐𝙉𝘿≽
<b>➤ This COMMAND IS WRONG...!!!!

➤ Use CORRECT COMMAND With Help
 Of The Channel Given Below</b>⍗
┗━━━━━𓆩𝘛𝘦𝘳𝘢𝘉𝘰𝘹𓆪ꪾ━━━━━┛"""

START_MESSAGE = "┏━━━━𓆩𝘌𝘳𝘳𝘰𝘳 𝘍𝘰𝘶𝘯𝘥𓆪ꪾ━━━━┓\n ♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 : {} \n\n ≼𝙄𝙈𝙋𝙊𝙍𝙏𝘼𝙉𝙏≽ \n **➤ If You Want To Use BOT, You \nHave To JOIN Both Channels. \n\n ➤IF You Facing Any Problem You \nCan Click On Tutorial Button ⇊** \n ┗━━━━━𓆩𝘛𝘦𝘳𝘢𝘉𝘰𝘹𓆪ꪾ━━━━━┛"

TRY_AGAIN_TEXT = "┏━━━━𓆩𝘌𝘳𝘳𝘰𝘳 𝘍𝘰𝘶𝘯𝘥𓆪ꪾ━━━━┓\n♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 : {} \n\n≼𝗪𝗔𝗥𝗡𝗜𝗡𝗚 𝗔𝗟𝗘𝗥𝗧≽\n➤ **Before Use. ME You Have To Must\nJOIN Both Channels\n\n➤ Please JOIN It And When You JOINED \nBoth Channels Then ♻️Try Again** \n┗━━━━━𓆩𝘛𝘦𝘳𝘢𝘉𝘰𝘹𓆪ꪾ━━━━━┛"

SU_TEXT = """🎉 𝗖𝗼𝗻𝗴𝗿𝗮𝘁𝘂𝗹𝗮𝘁𝗶𝗼𝗻𝘀  {}

≼𝙎𝙪𝙥𝙚𝙧 𝙐𝙨𝙚𝙧≽ :
**➤  Now You Can Store Data Easily If You Dont Know How to Use It You Can See The Tutorial Video**

≼𝙄𝙈𝙋𝙊𝙍𝙏𝘼𝙉𝙏≽ :
**➤ If You Can See CONNECT Button 
SO You Want To Setup Before Use me**

<pre>𝙀𝙓𝙋𝙄𝙍𝙀 𝘼𝙏 ➤ {}</pre>"""

EXPIRE_TEXT = """
♛ 𝙃𝙚𝙮 𝙏𝙂 𝙐𝙨𝙚𝙧 :{}

≼𝙈𝙚𝙢𝙚𝙗𝙚𝙧𝙎𝙝𝙞𝙥 𝙀𝙭𝙥𝙞𝙧𝙚𝙙≽
**➤Sorry To Say {} But Your Plan 
Is Expired Now But You Can RENEW**

≼𝙁𝙊𝙍 𝙍𝙀𝙉𝙀𝙒≽ :
➤If You Want To RENEW Then You Have To Click On The Button Below.
"""

CUSTOM_CAPTION = """
Here is your file thanks for using me.
"""