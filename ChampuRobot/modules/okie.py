import os

import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO, BytesIO 
from time import time
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery 
import io
from ChampuRobot import app


excl = lambda cmd, prefixes=['/','.', '!'], cs=True: filters.command(cmd, prefixes, cs)

cmd = filters.command 

regex = filters.regex 

IKM =InlineKeyboardMarkup

IKB = InlineKeyboardButton 



CHAT_ID = 1302298741



async def aexec_(code, smessatatus, client):

    m = message = event = smessatatus

    p = lambda _x: print(yaml_format(_x))

    exec("async def __aexec(message, event, m, client, p): " +

         "".join(f"\n {l}" for l in code.split("\n")))

    return await locals()["__aexec"](message, event, m, client, p)





@app.on_edited_message(excl('eval'))

@app.on_message(excl('eval'))

async def eval(client, message):

    if message.from_user.id != 1302298741:

        return

    if len(message.command) == 1:

        return await message.reply("What You Want To Stuff")

    cmd = "".join(message.text.split(None, 1)[1:])

    if "config.py" in cmd:

        return await message.reply_text(

            "#PRIVACY_ERROR\nCan't access config.py`",

            reply_to_message_id=message.id)

    print(cmd)

    if not cmd:

        return await message.reply_text("What should I run?", reply_to_message_id=message.id)

    eva = await message.reply_text("Running...", reply_to_message_id=message.id)

    old_stderr = sys.stderr

    old_stdout = sys.stdout

    redirected_output = sys.stdout = io.StringIO()

    redirected_error = sys.stderr = io.StringIO()

    stdout, stderr, exc = None, None, None

    try:

        await aexec_(cmd, message, client)

    except Exception:

        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()

    stderr = redirected_error.getvalue()

    sys.stdout = old_stdout

    sys.stderr = old_stderr

    evaluation = ""

    if exc:

        evaluation = exc

    elif stderr:

        evaluation = stderr

    elif stdout:

        evaluation = stdout

    else:

        evaluation = "Success"

    final_output = (

        f"⥤ ᴇᴠᴀʟ : \n<pre>{cmd}</pre> \n\n⥤ ʀᴇsᴜʟᴛ : \n<pre>{evaluation}</pre>"

    )

    if len(final_output) > 4096:

        filename = "result.txt"

        with open(filename, "w+", encoding="utf8") as out_file:

            out_file.write(str(evaluation.strip()))

        keyboard = IKM([[

            IKB(

                text="🗑",

                callback_data="evclose",

            )

        ]])

        '''bimsi = await app.send_document(chat_id=CHAT_ID,

            document=filename,

            caption=

            f"**INPUT:**\n`cmd[0:980]`\n\n**OUTPUT:**\n`Attached Document`",

            reply_markup=keyboard)

        await message.reply(f"Your : [Result]({bimsi.link})",parse_mode=enums.ParseMode.MARKDOWN)'''

        await message.reply_document(document=filename, caption=f"**INPUT:**\n`cmd[0:980]`\n\n**OUTPUT:**\n`Attached Document`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)

        await eva.delete()

        os.remove(filename)

    else:

        keyboard = IKM([[

            IKB(

                text="🗑",

                callback_data="evclose",

            )

        ]])

        await eva.edit_text(text=final_output, reply_markup=keyboard)





@app.on_callback_query(regex('^evclose$'), group=50)

async def closer(client, q):

    if q.from_user.id != q.message.reply_to_message.from_user.id:

        return

    await q.message.delete()
