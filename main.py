import pyrogram, os, asyncio

# Environment Variables
try: app_id = int(os.environ.get("app_id", "20389440"))
except Exception as app_id: print(f"⚠️ App ID Invalid {app_id}")
try: api_hash = os.environ.get("api_hash", "a1a06a18eb9153e9dbd447cfd5da2457")
except Exception as api_id: print(f"⚠️ Api Hash Invalid {api_hash}")
try: bot_token = os.environ.get("bot_token", "6564513574:AAH3Y97iqQjSlV5vKKZdGDUohlhpA-LeSbw")
except Exception as bot_token: print(f"⚠️ Bot Token Invalid {bot_token}")

# Initialize the Bot
AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token)

# Replacement Mapping (Define your replacements here)
replacement_dict = {
    "@demon_0214": "[𝑴𝑨𝑯𝑰®🇮🇳](https://t.me/+TQfNhTbrVC04NWNl)",
    "Extracted by:": "𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 ➤",
    "जय श्री राम 🚩🚩": "Coaching ➤ Kalam Academy Sikar",
    # Add more replacements as needed
}

# Function to replace words in a caption
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
        pyrogram.types.InlineKeyboardButton("Updates", url="t.me/MAHI_BOTZ"),
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
print("Telegram AutoCaption V7 Bot Start")
print("Bot Created By MAHI®")

AutoCaptionBotV1.run()

