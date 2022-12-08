from pyrogram import Client, filters
from pyrogram.types import Message
hl = "."
from Zaid.database.sudo import *

async def eor(m: Message, t):
    try:
        await m.edit(t)
    except:
        await m.reply(t)
        
async def get_id(m: Message):
    if str(m.chat.id)[0] != "-":
        return int(m.chat.id)
    if not m.reply_to_message:
        text = m.text.split()
        un_or_id = text[1]
        if un_or_id[0] == "@":
            id = (await _.get_users(un_or_id)).id
        else:
            id = int(un_or_id)
    else:
        id = m.reply_to_message.from_user.id
    return id 

@Client.on_message(filters.command(["addsudo", "rmsudo"], "."))
async def add_or_del_sudo(_, m):
    me = await _.get_me()
    if m.from_user.id != me.id:
        return
    try:
        id = await get_id(m)
    except:
        return await eor(m, f"<i>{hl}addsudo or {hl}rmvsudo [Reply | Username | Id]</id>")
    sudo = await is_sudo(id)
    if m.text.split()[0][1].lower() == "r":
        if not sudo:
            return await eor(m, f"<i>This user isn't sudo..!</i>")
        await del_sudo(id)
        return await eor(m, f"<i>Sudo removed for the user {id} .</i>")
    if sudo:
        return await eor(m, f"<i>{id} is already a sudo user..!</i>")
    await add_sudo(id)
    return await eor(m, f"<i>{id} is added to sudo...!</i>")

@Client.on_message(filters.command("sudos", "."))
async def sudo_users(_, m):
    me = await _.get_me()
    sudo = await is_sudo(m.from_user.id)
    if m.from_user.id != me.id and not sudo:
        return
    SUDOS = await get_sudos()
    if not SUDOS:
        return await eor(m, f"<i>No sudo users..!</i>")
    msg = ""
    for SUDO in SUDOS:
        SUDO = int(SUDO)
        msg += f"\n<code>{SUDO}</code>"
    return await eor(m, f"<i>Sudo :-</i>\n{msg}\n\n<i>Count :- {len(SUDOS)}</i>")
