import html
import os

import nekos
import requests
from PIL import Image
from telegram import Update
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

import ChampuRobot.modules.sql.nsfw_sql as sql
from ChampuRobot import dispatcher
from ChampuRobot.modules.helper_funcs.chat_status import user_admin
from ChampuRobot.modules.helper_funcs.filters import CustomFilters
from ChampuRobot.modules.log_channel import gloggable


@run_async
@user_admin
@gloggable
def add_nsfw(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        sql.set_nsfw(chat.id)
        msg.reply_text("ᴀᴄᴛɪᴠᴀᴛɪᴏɴ ɴsғᴡ ᴍᴏᴅᴇ!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ᴀᴄᴛɪᴠᴀᴛᴇᴅ_ɴsғᴡ\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("ɴsғᴡ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ")
        return ""


@run_async
@user_admin
@gloggable
def rem_nsfw(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        msg.reply_text("ɴsғᴡ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return ""
    else:
        sql.rem_nsfw(chat.id)
        msg.reply_text("ʀᴏʟʟᴇᴅ ʙᴀᴄᴋ ᴛᴏ ɴsғᴡ ᴍᴏᴅᴇ")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ_ɴsғᴡ\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message


def list_nsfw_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_nsfw_chats()
    text = "<b>ɴsғᴡ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴄʜᴀᴛs</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title if x.title else x.first_name
            text += f"• <code>{name}</code>\n"
        except BadRequest:
            sql.rem_nsfw(*chat)
        except Unauthorized:
            sql.rem_nsfw(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")


def neko(update, context):
    msg = update.effective_message
    target = "neko"
    msg.reply_photo(nekos.img(target))

def wallpaper(update, context):
    msg = update.effective_message
    target = "wallpaper"
    msg.reply_photo(nekos.img(target))


def tickle(update, context):
    msg = update.effective_message
    target = "tickle"
    msg.reply_video(nekos.img(target))


def feed(update, context):
    msg = update.effective_message
    target = "feed"
    msg.reply_video(nekos.img(target))

def waifu(update, context):
    msg = update.effective_message
    target = "waifu"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


def kiss(update, context):
    msg = update.effective_message
    target = "kiss"
    msg.reply_video(nekos.img(target))

def hug(update, context):
    msg = update.effective_message
    target = "cuddle"
    msg.reply_video(nekos.img(target))

def smug(update, context):
    msg = update.effective_message
    target = "smug"
    msg.reply_video(nekos.img(target))


def dva(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            return
    msg = update.effective_message
    nsfw = requests.get("https://api.computerfreaker.cf/v1/dva").json()
    url = nsfw.get("url")
    # do shit with url if you want to
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_photo(url)


ADD_NSFW_HANDLER = CommandHandler("addnsfw", add_nsfw)
REMOVE_NSFW_HANDLER = CommandHandler("rmnsfw", rem_nsfw)
LIST_NSFW_CHATS_HANDLER = CommandHandler(
    "nsfwchats", list_nsfw_chats, filters=CustomFilters.dev_filter
)
NEKO_HANDLER = CommandHandler("neko", neko)
WALLPAPER_HANDLER = CommandHandler("wallpaper", wallpaper)
TICKLE_HANDLER = CommandHandler("tickle", tickle)
FEED_HANDLER = CommandHandler("feed", feed)
WAIFU_HANDLER = CommandHandler("waifu", waifu)
KISS_HANDLER = CommandHandler("kiss", kiss)
CUDDLE_HANDLER = CommandHandler("hug", hug)
SMUG_HANDLER = CommandHandler("smug", smug)


dispatcher.add_handler(ADD_NSFW_HANDLER)
dispatcher.add_handler(REMOVE_NSFW_HANDLER)
dispatcher.add_handler(LIST_NSFW_CHATS_HANDLER)
dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)
dispatcher.add_handler(KISS_HANDLER)
dispatcher.add_handler(CUDDLE_HANDLER)
dispatcher.add_handler(SMUG_HANDLER)

__handlers__ = [
    ADD_NSFW_HANDLER,
    REMOVE_NSFW_HANDLER,
    LIST_NSFW_CHATS_HANDLER,
    NEKO_HANDLER,
    WALLPAPER_HANDLER,
    TICKLE_HANDLER,
    FEED_HANDLER,
    WAIFU_HANDLER,
    KISS_HANDLER,
    CUDDLE_HANDLER,
    SMUG_HANDLER,
]
__mod_name__ = "Nsғᴡ"

__help__ = """
*ɴsғᴡ:*
❂ /addnsfw  : ᴇɴᴀʙʟᴇ ɴsғᴡ ᴍᴏᴅᴇ
❂ /rmnsfw  : ᴅɪsᴀʙʟᴇ ɴsғᴡ ᴍᴏᴅᴇ
 
*ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:*  
❂ /neko : sᴇɴᴅs ʀᴀɴᴅᴏᴍ sғᴡ ɴᴇᴋᴏ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.
❂ /tickle : sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴛɪᴄᴋʟᴇ ɢɪғs.
❂ /feed : sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴇᴇᴅɪɴɢ ɢɪғs.
❂ /waifu : sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜ sᴛɪᴄᴋᴇʀs.
❂ /kiss : sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴋɪssɪɴɢ ɢɪғs.
❂ /smug : sᴇɴᴅs ʀᴀɴᴅᴏᴍ sᴍᴜɢ ɢɪғs.
❂ /wallpaper : sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀʟʟᴘᴀᴘᴇʀ.
"""
