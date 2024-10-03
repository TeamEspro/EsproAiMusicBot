from pyrogram import Client, filters
import re
from EsproAiMusic import app


# Sticker forward karne wala function
@app.on_message(filters.command("set", prefixes="/") & filters.group)
async def set_sticker_target(client, message):
    # Command mein username ko tag karna
    if len(message.command) > 1:
        target_username = message.command[1].replace("@", "")  # Username extract karna

        # Check karen agar user group mein hai ya nahi
        try:
            target_user = await client.get_chat_member(message.chat.id, target_username)
            await message.reply(f"Sticker is set for @{target_username}. Only they can see the sticker.")
        except:
            await message.reply(f"User @{target_username} is not in this group.")
    else:
        await message.reply("Please tag a user using the /set command.")

# Sticker handle karne wala function
@app.on_message(filters.sticker & filters.group)
async def handle_sticker(client, message):
    if message.reply_to_message and message.reply_to_message.from_user.username:
        target_username = message.reply_to_message.from_user.username  # Sticker jis user ko tag karke bheja gaya
        
        # Check karen agar sticker dekhne wala user tag kiya gaya user hai ya nahi
        if message.from_user.username == target_username:
            await message.reply(f"Sticker aapko dikhaya gaya hai, @{target_username}.")
        else:
            await message.delete()  # Agar sender aur target user match nahi karte to sticker delete kar do
    else:
        await message.reply("Please use /set command to send a sticker to a specific user.")

