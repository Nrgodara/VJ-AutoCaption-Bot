import pyrogram, os, asyncio

# Environment Variables
try: app_id = int(os.environ.get("app_id", "24825870"))
except Exception as app_id: print(f"⚠️ App ID Invalid {app_id}")
try: api_hash = os.environ.get("api_hash", "12ab9061b6260f9b91632947331ea0f6")
except Exception as api_id: print(f"⚠️ Api Hash Invalid {api_hash}")
try: bot_token = os.environ.get("bot_token", "7162644889:AAFKmJtOSYMbeIf3QWAGgcR0FZqZv85Sakg")
except Exception as bot_token: print(f"⚠️ Bot Token Invalid {bot_token}")

# Initialize the Bot
AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token)

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>@VJ_Botz</b>"""

about_message = """
<b>• Name : <a href=https://t.me/VJ_Botz>VJ AutoCaption</a></b>
<b>• Developer : <a href=https://t.me/VJ_Botz>[VJ UPDATES]</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/VJ_Botz>Click Here</a></b>
<b>• Source Code : <a href=https://github.com/VJBots/VJ-AutoCaption-Bot>Click Here</a></b>"""


# Replacement Mapping (Define your replacements here)
replacement_dict = {
    "@demon_0214": "[𝑴𝑨𝑯𝑰®🇮🇳](https://t.me/+TQfNhTbrVC04NWNl)",
    "Extracted by:": "𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 ➤",
    "जय श्री राम 🚩🚩": "Coaching ➤ Kalam Academy Sikar",
    "Unrestricted by Team SPY": "",
    "MR Joker": "",
    "@MK_rj49 🚩": "[𝑴𝑨𝑯𝑰®🇮🇳](https://t.me/+TQfNhTbrVC04NWNl)",
    "Downloaded by:": "𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 ➤",
    
    # Add more replacements as needed
}

# List of words to delete from the caption
words_to_delete = [
    "Unrestricted by Team SPY",
    "MR Joker",
    # Add more words to delete as needed
]

# Function to replace and delete words in a caption
def replace_words(caption, replacements):
    for old_word, new_word in replacements.items():
        caption = caption.replace(old_word, new_word)
    return caption

# Start Command Handler
@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

# Callback Query Handlers
@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("start"))
def start_callback(bot, update):
    update.message.edit(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(about_message.format(version=pyrogram.__version__, username=bot.mention), reply_markup=about_buttons(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

# Channel Message Handler to Edit Caption
@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    motech, _ = get_file_details(update)
    
    # Only proceed if there is a caption
    if update.caption:
        # Replace words in the caption
        new_caption = replace_words(update.caption, replacement_dict)
        new_caption += "\n𝔼𝕏ℙ𝔼ℂ𝕋 𝕋ℍ𝔼 𝕌ℕ𝔼𝕏ℙ𝔼ℂ𝕋𝔼𝔻 🫰❤️‍🔥\n•┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈•\n       **@Free_Batches_bot** "
        
        try:
            try:
                update.edit(new_caption)
            except pyrogram.errors.FloodWait as FloodWait:
                asyncio.sleep(FloodWait.value)
                update.edit(new_caption)
        except pyrogram.errors.MessageNotModified:
            pass

# Function to Get File Details
def get_file_details(update: pyrogram.types.Message):
    if update.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id

# Functions for Buttons
def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [[
        pyrogram.types.InlineKeyboardButton("Updates", url="t.me/mahi_Botz"),
        pyrogram.types.InlineKeyboardButton("About 🤠", callback_data="about")
    ], [
        pyrogram.types.InlineKeyboardButton("➕️ Add To Your Channel ➕️", url=f"http://t.me/{bot.username}?startchannel=true")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [[
        pyrogram.types.InlineKeyboardButton("🏠 Back To Home 🏠", callback_data="start")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

# Start the Bot
print("Telegram AutoCaption V1 Bot Start")
print("Bot Created By https://t.me/Mahi_botz")

AutoCaptionBotV1.run()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
