import os
import requests
# from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# load_dotenv()
UNSCREEN_API = "EC8JuKQbKRg3W5JdQqHLmKiS"
REMOVEBG_API = "kZTKztjYGsGo155mywFTH3Fe"

BGRBot = Client(
    "Remove Background Bot",
    bot_token="5377088293:AAGCUktSt5vLfTx2brzBsurvlU-yYT2PHXQ",
    api_id=18988485,
    api_hash="b8b78728c7f08859bfa98f5cbb250dc8"
)

START_TEXT = """**🙌 Hello {},

I am a media background remover bot.
Send me a photo or video I will send the media without background.

@PyroBotz**"""


START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✅ 𝗠𝗼𝗿𝗲 𝗕𝗼𝘁𝘇 ✅', url='https://t.me/PyroBotz')
        ],[
            InlineKeyboardButton('🐞 𝖱𝖾𝗉𝗈𝗋𝗍 𝖡𝗎𝗀 🐞', url='https://t.me/PYRO_BOTZ_CHAT')
        ]
    ]
)

ERROR_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🐞 𝖱𝖾𝗉𝗈𝗋𝗍 𝖡𝗎𝗀 🐞', url='https://t.me/PYRO_BOTZ_CHAT')
        ]
    ]
)

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✅ 𝗝𝗢𝗜𝗡 𝗡𝗢𝗪 ✅', url='https://t.me/PyroBotz')
        ]
    ]
)

@BGRBot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update, cb=False):
    text=START_TEXT.format(update.from_user.mention)
    if cb:
        await update.message.edit_text(
            text=text,
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS,
            quote=True
        )

@BGRBot.on_message(filters.private & (filters.photo | filters.video | filters.document))
async def remove_background(bot, update):
    if not (REMOVEBG_API or UNSCREEN_API):
        await update.reply_text(
            text="Error :- API not found",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Processing",
        quote=True,
        disable_web_page_preview=True
    )
    try:
        new_file_name = f"./{str(update.from_user.id)}"
        if (
            update.photo or (
                update.document and "image" in update.document.mime_type
            )
        ):
            new_file_name += ".png"
            file = await update.download()
            await message.edit_text(
                text="Photo downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_image(file)
        elif (
            update.video or (
                update.document and "video" in update.document.mime_type
            )
        ):
            new_file_name += ".webm"
            file = await update.download()
            await message.edit_text(
                text="Video downloaded successfully. Now removing background.",
                disable_web_page_preview=True
            )
            new_document = removebg_video(file)
        else:
            await message.edit_text(
                text="Media not supported",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
        try:
            os.remove(file)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=error,
            disable_web_page_preview=True
        )
    try:
        with open(new_file_name, "wb") as file:
            file.write(new_document.content)
        await update.reply_chat_action("upload_document")
    except Exception as error:
        await message.edit_text(
           text=error,
           reply_markup=ERROR_BUTTONS
        )
        return
    try:
        await update.reply_document(
            document=new_file_name,
            quote=True
        )
        try:
            os.remove(new_file_name)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=f"Error:- `{error}`",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )


def removebg_video(file):
    return requests.post(
        "https://api.unscreen.com/v1.0/videos",
        files={"video_file": open(file, "rb")},
        headers={"X-Api-Key": UNSCREEN_API}
    )
