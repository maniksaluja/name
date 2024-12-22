from os import getenv

# Ensure FSUB_1 and FSUB_2 are defined
#Make sure you give channel id of those channel in which you want to create join request in RFSUB
FSUB_1 = int(getenv('FSUB_1', '-1001685428564')) #This chat will not create join request
FSUB_2 = int(getenv('FSUB_2', '-1002111057093')) #This chat will not create join request
RFSUB  = [int(i) for i in getenv("RFSUB", "-1001586309125").split()] #Give space spearated value of the channel which you want that user will create a join request for leave it 0 if you don't want any request type force sub

# Now define FSUB using FSUB_1 and FSUB_2
FSUB = [FSUB_1, FSUB_2]

# Load other values from environment variables
API_ID = int(getenv('API_ID', '26980824'))
API_HASH = getenv('API_HASH', 'fb044056059384d3bea54ab7ce915226')

# Add separate API ID and API Hash for both bots
API_ID2 = int(getenv('API_ID_BOT1', '3510496'))  # Bot2 API ID
API_HASH2 = getenv('API_HASH_BOT1', 'c65647776bb4e93defc9504571d2b990')  # Bot2 API Hash

#Bot token for the bot
BOT_TOKEN = getenv('BOT_TOKEN', '1766393685:AAG6qNwLEuIVe3frjqSGhjYDseS3eRkeqDs')
BOT_TOKEN_2 = getenv('BOT_TOKEN_2', '5458055532:AAE8SqugCY-gIsQMrVvyV5f53duBr18dyJ4')

BUY_LINK = "t.me/iamgojoof6eyes" #Link to the acc or channel on which user will be redirected when he clicks on Buy now in voice msg
OWNER_ID =1344569458
SUDO_USERS = []
SUDO_USERS.append(OWNER_ID)
MONGO_DB_URI= "mongodb+srv://Gojo:gojoisded@test.m08k4kx.mongodb.net/?retryWrites=true&w=majority&appName=Test"

#All the essential channels needed
DB_CHANNEL_ID = int(getenv('DB_CHANNEL_ID', '-1002094195888'))
DB_CHANNEL_2_ID = int(getenv('DB_CHANNEL_2_ID', '-1002094195888'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', '-1001685428564'))
LOG_CHANNEL_ID2 = int(getenv('LOG_CHANNEL_ID2', '-1002111057093')) #Keep it 0 if you don't have second log channel
FEEDBACK_CHANNEL = int(getenv("FEEDBACK_CHANNEL", -1001685428564)) # Keep it 0 if you don't want to give feed back channel id
AFTER_FEEDBACK = int(getenv("AFTER_FEEDBACK", -1002111057093)) #Channel on which post will be forwarded when the owner clicks on approve
AUTO_SAVE_CHANNEL = int(getenv("AUTO_SAVE_CHANNEL", -1001685428564)) #Channel where all the content from fsub1 will be saved

AUTO_DELETE_TIME = int(getenv('AUTO_DELETE_TIME', '60'))  # Enter time in seconds, keep it 0 for disabling.

MUST_VISIT_LINK = "https://t.me/Ultra_XYZ/14"

LINK_GENERATE_IMAGE = getenv('LINK_GENERATE_IMAGE', 'https://graph.org/file/a1cce5b8533180c2f0029.jpg')

TUTORIAL_LINK = getenv('TUTORIAL_LINK', 'https://t.me/Ultra_XYZ/16')

CONNECT_TUTORIAL_LINK = getenv('CONNECT_TUTORIAL_LINK', 'https://t.me/Terabox_Sharing_Bot?start=batchoneaWZkYS1pZmRjfGhoZg==')
SU_IMAGE = "https://graph.org/file/2342d37844afd1b9b96c0.jpg"

JOIN_MESSAGE = getenv('JOIN_MESSAGE', 'You Joined.')
JOIN_IMAGE = getenv('JOIN_IMAGE', 'https://graph.org/file/015fddf0dbeb03b639647.jpg')

LEAVE_CAPTION = getenv('LEAVE_CAPTION', 'I Love You.')

USELESS_MESSAGE = getenv('USELESS_MESSAGE', 'This is useless text.')
USELESS_IMAGE = getenv('USELESS_IMAGE', 'https://graph.org/file/c579032c65d8353e43b0f.jpg')

STICKER_ID = 'CAACAgUAAxkBAAIiHWZjPezFGPWT_87VHnJUaschvGtrAAJtDgACYpoYV06rLlLA8dv_HgQ'

CONTENT_SAVER = True

EXPIRY_TIME = 30  # In days

AUTO_SAVE_CHANNEL_ID = -1001685428564

PHONE_NUMBER_IMAGE = "https://graph.org/file/2821554b6b082eb8741dc.jpg"

WARN_IMAGE = 'https://graph.org/file/c86c68e014e471c1ce729.jpg'
