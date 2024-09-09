import asyncio
from EsproAiMusic import app
from pyrogram import filters

# List of offensive or pornographic sticker set names
BANNED_STICKER_SETS = [
    "porn", "nsfw", "xxx", "sex", "18+", "explicit", "adult", "nude", "xxxrated"
]

# Function to detect and delete offensive stickers
@app.on_message(filters.sticker & filters.group)
async def remove_porn_stickers(client, message):
    sticker = message.sticker

    # Check if the sticker belongs to a banned set based on its name
    if sticker.set_name and any(banned in sticker.set_name.lower() for banned in BANNED_STICKER_SETS):
        try:
            # Delete the sticker message
            await message.delete()

            # Send a warning message after deletion
            warning_message = await client.send_message(
                chat_id=message.chat.id,
                text="🚫 **Pornographic sticker has been deleted. Please avoid sending such content!**",
            )

            # Wait for 10 seconds before deleting the warning message
            await asyncio.sleep(10)
            await client.delete_messages(chat_id=member.chat.id, message_ids=message.id)


        except Exception as e:
            print(f"Error while deleting sticker: {e}")
