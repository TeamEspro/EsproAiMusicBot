from EsproAiMusic import app
from pyrogram import filters
import re

# Define a URL pattern
URL_PATTERN = re.compile(r"(https?://[^\s]+)")

# Function to detect and delete messages with links
@app.on_message(filters.group & filters.text)
async def delete_link_messages(client, message):
    if URL_PATTERN.search(message.text):  # Check if the message contains a link
        try:
            await message.delete()  # Delete the message
            print(f"Deleted a message with link from {message.from_user.mention}")
        except Exception as e:
            print(f"Failed to delete message: {e}")

# The bot will monitor the group for any message that contains a link and delete it
