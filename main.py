import pyrogram
import os
import asyncio




try:
    app_id = int(os.environ.get("app_id", "20389440"))
except Exception as app_id:
    print(f"⚠️ App ID Invalid {app_id}")

try:
    api_hash = os.environ.get("api_hash", "a1a06a18eb9153e9dbd447cfd5da2457")
except Exception as api_id:
    print(f"⚠️ Api Hash Invalid {api_hash}")

try:
    bot_token = os.environ.get("bot_token", "6564513574:AAH3Y97iqQjSlV5vKKZdGDUohlhpA-LeSbw")
except Exception as bot_token:
    print(f"⚠️ Bot Token Invalid {bot_token}")

try:
    custom_caption = os.environ.get("custom_caption", "`{file_name}`")
except Exception as custom_caption:
    print(f"⚠️ Custom Caption Invalid {custom_caption}")

try:
    custom_footer = os.environ.get("custom_footer", "")
except Exception as custom_footer:
    print(f"⚠️ Custom Footer Invalid {custom_footer}")

try:
    delete_text = os.environ.get("delete_text", "del")
except Exception as delete_text:
    print(f"⚠️ Delete Text Invalid {delete_text}")

AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token
)

start_message = """
<b>👋Hello {}❤️‍🔥</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power🧿</b>
<b>@VJ_Botz</b>"""

about_message = """
<b>• Name : <a href=http://t.me/Fhgffghhrbot</a></b>
<b>• Developer : <a href=MAHI® BOSS 🤭</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/defence_exams_all>Click Here</a></b>
<b>• Source Code : <a href=https://github.com/Nrgodara/VJ-AutoCaption-Bot>Click Here</a></b>"""

@AutoCaptionBotV1.on_message(pyrogram.filters.channel & (pyrogram.filters.video | pyrogram.filters.document))
def edit_caption(bot, update: pyrogram.types.Message):
    motech, _ = get_file_details(update)

    try:
        # Get existing caption or set it to an empty string if there's none
        existing_caption = update.caption if update.caption else ""

        # Add a footer to the caption
        new_caption = f"{existing_caption}\n\nCustom Footer: {custom_footer}"

        # Check for a "delete" text and remove it
        new_caption = new_caption.replace(delete_text, "").strip()

        try:
            update.edit(new_caption)
        except pyrogram.errors.FloodWait as FloodWait:
            asyncio.sleep(FloodWait.value)
            update.edit(new_caption)
    except pyrogram.errors.MessageNotModified:
        pass

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["setdel"]))
def set_delete_text(bot, update):
    try:
        # Get the text following the "/setdel" command
        delete_text = " ".join(update.command[1:]).strip()

        # Set the delete text in the environment variable
        os.environ["delete_text"] = delete_text

        update.reply(f"Delete text set to: `{delete_text}`")
    except Exception as e:
        update.reply(f"Error setting delete text: {e}")

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["deldel"]))
def delete_delete_text(bot, update):
    try:
        # Remove the delete text from the environment variable
        os.environ.pop("delete_text", None)

        update.reply("Delete text cleared.")
    except Exception as e:
        update.reply(f"Error clearing delete text: {e}")

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["footer"]))
def set_footer_text(bot, update):
    try:
        # Get the text following the "/footer" command
        custom_footer = " ".join(update.command[1:]).strip()

        # Set the custom footer in the environment variable
        os.environ["custom_footer"] = custom_footer

        update.reply(f"Custom footer set to: `{custom_footer}`")
    except Exception as e:
        update.reply(f"Error setting custom footer: {e}")

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["delfooter"]))
def delete_footer_text(bot, update):
    try:
        # Remove the custom footer from the environment variable
        os.environ.pop("custom_footer", None)

        update.reply("Custom footer cleared.")
    except Exception as e:
        update.reply(f"Error clearing custom footer: {e}")

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["free"]))
def reset_actions(bot, update):
    try:
        # Remove all environment variables related to customization
        os.environ.pop("custom_footer", None)
        os.environ.pop("delete_text", None)

        update.reply("Bot actions reset. Custom footer and delete text cleared.")
    except Exception as e:
        update.reply(f"Error resetting bot actions: {e}")

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("start"))
def start_callback(bot, update):
    update.message.edit(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(
        about_message.format(version=pyrogram.__version__, username=bot.mention),
        reply_markup=about_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    motech, _ = get_file_details(update)

    try:
        try:
            update.edit(custom_caption.format(file_name=motech.file_name))
        except pyrogram.errors.FloodWait as FloodWait:
            asyncio.sleep(FloodWait.value)
            update.edit(custom_caption.format(file_name=motech.file_name))
    except pyrogram.errors.MessageNotModified:
        pass

def get_file_details(update: pyrogram.types.Message):
    if update.media:
        for message_type in (
            #"photo",
            #"animation",
            #"audio",
            "document",
            "video",
            "video_note",
            "voice",
            # "contact",
            # "dice",
            # "poll",
            # "location",
            # "venue",
            #"sticker",
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id

def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [
        [
            pyrogram.types.InlineKeyboardButton(
                "Updates", url="t.me/VJ_Botz"
            ),
            pyrogram.types.InlineKeyboardButton(
                "About 🤠", callback_data="about"
            ),
        ],
        [
            pyrogram.types.InlineKeyboardButton(
                "➕️ Add To Your Channel ➕️",
                url=f"http://t.me/{bot.username}?startchannel=true",
            )
        ],
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [
        [pyrogram.types.InlineKeyboardButton("🏠 Back To Home 🏠", callback_data="start")]
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

print("Telegram AutoCaption Bot Start")
print("Bot Created By **MAHI®⚡**")

AutoCaptionBotV1.run()
