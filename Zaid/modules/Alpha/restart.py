from pyrogram import Client, filters
from Zaid import SUDO_USER
import os

@Client.on_message(filters.command("restart", ".") & (filters.me | filters.user(SUDO_USER)))
async def resta(_, m):
    ok = await m.reply("Restarting...")
    os.system(f"kill -9 {os.getpid()} && python3 -m Zaid")
    try:
      await ok.edit("Restarted !")
    except:
      pass
