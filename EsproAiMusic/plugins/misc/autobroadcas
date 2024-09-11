import asyncio
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from EsproAiMusic import app
from config import START_IMG_URL
from EsproAiMusic.utils.database import get_served_chats

MESSAGE = f"""**๏ ᴛʜɪs ɪs ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs + ᴄʜᴀɴɴᴇʟs ᴠᴄ. 💌

🎧 ᴘʟᴀʏ + ᴠᴘʟᴀʏ + ᴄᴘʟᴀʏ 🎧

➥ sᴜᴘᴘᴏʀᴛᴇᴅ ᴡᴇʟᴄᴏᴍᴇ - ʟᴇғᴛ ɴᴏᴛɪᴄᴇ, ᴛᴀɢᴀʟʟ, ᴠᴄᴛᴀɢ, ʙᴀɴ - ᴍᴜᴛᴇ, sʜᴀʏʀɪ, ʟᴜʀɪᴄs, sᴏɴɢ - ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ, ᴇᴛᴄ... 💕

🔐ᴜꜱᴇ » [/start](https://t.me/{app.username}?start=help) ᴛᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ

➲ ʙᴏᴛ :** @{app.username}"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
        ],
        [
            InlineKeyboardButton("๏ 𝗙𝐚𝐦𝐢𝐥𝐲 ටƒ 𝗙𝐫𝐢𝐞𝐧𝐝𝐬𝐡𝐢𝐩 ✨ ๏", url=f"https://t.me/FamilyOfFriendship")
        ]
    ]
)

async def send_message_to_chats():
    try:
        chats = await get_served_chats()

        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    # Send the message and capture the sent message
                    sent_message = await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    
                    # Wait for 20 seconds before deleting the message
                    await asyncio.sleep(20)
                    
                    # Delete the message after 20 seconds
                    await app.delete_messages(chat_id, sent_message.message_id)
                except Exception as e:
                    print(f"Error sending or deleting message: {e}")  # Log the error
    except Exception as e:
        print(f"Error fetching served chats: {e}")  # Log the error

async def continuous_broadcast():
    while True:
        await send_message_to_chats()
        await asyncio.sleep(3600)  # Sleep for 1 hour (3600 seconds) between broadcasts

# Start the client and the continuous broadcast loop
if __name__ == "__main__":
    app.run()  # Ensure the client is running
    asyncio.create_task(continuous_broadcast())
