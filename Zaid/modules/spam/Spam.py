import asyncio
from re import sub
from threading import Event
import time
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import LOG_GROUP
from Zaid import SUDO_USER 

from Zaid.modules.help import add_command_help

commands = ["spam", "statspam", "slowspam", "fastspam"]
SPAM_COUNT = [0]

BLACKLIST_CHAT = []
BLACKLIST_CHAT.append(-1001521704453)



def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50

async def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ""

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if " " not in text:
        return ""

    text = sub(r"\s+", " ", text)
    text = text[text.find(" ") :].strip()
    return text

@Client.on_message(
    filters.command(["dspam", "delayspam"], ".") & (filters.me | filters.user(SUDO_USER))
)

async def delayspam(client: Client, message: Message):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    try:
        delay = float(message.text.split()[1])
        count = int(message.text.split()[2])
        txt = message.text.split(None, 3)[3]
    except:
        return await message.reply("Babu thoda dekha kro !")
    for i in range(0, count):
        await client.send_message(message.chat.id, txt)
        time.sleep(delay)


@Client.on_message(
    filters.command(commands, ".") & (filters.me | filters.user(SUDO_USER))
)
async def sspam(client: Client, message: Message):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    cooldown = {"spam": 0.15, "statspam": 0.1, "slowspam": 0.9, "fastspam": 0}

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])


@Client.on_message(
    filters.command(["sspam", "stkspam", "spamstk", "stickerspam"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def spam_stick(client: Client, message: Message):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    if not message.reply_to_message:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    if not message.reply_to_message.sticker:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    else:
        i = 0
        times = message.command[1]
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)


add_command_help(
    "spam",
    [
        ["spam <amount of spam> <text>", "Spamming texts in chats!!"],
        [
            "delayspam <seconds> <amount of spam> <text>",
            "Send spam text with a specified delay period!",
        ],
    ],
)
