from pyrogram import filters
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pyrogram.types import ChatPermissions
import re
from EsproAiMusic import app

# Regex pattern to detect URLs in the bio
url_pattern = re.compile(r"(https?://[^\s]+|www\.[^\s]+)")

# Function to detect new members and mute them if they have links in their bio
@app.on_message(filters.new_chat_members)
async def auto_mute_new_member(_, message):
    new_members = message.new_chat_members
    chat_id = message.chat.id

    for new_member in new_members:
        user_id = new_member.id
        try:
            # Fetch user details
            user = await app.get_users(user_id)

            # Check if the bio contains a link
            if user.bio and url_pattern.search(user.bio):
                # If the bio contains a link, mute the member
                try:
                    await app.restrict_chat_member(
                        chat_id,
                        user_id,
                        ChatPermissions(can_send_messages=False)  # Mute the member
                    )
                    await message.reply_text(f"🚫 {user.first_name} has been muted because their bio contains a link.")
                except ChatAdminRequired:
                    # If bot lacks admin permissions, notify the group owner/admin
                    await message.reply_text(
                        "⚠️ I need admin rights with 'Ban Members' permission to mute members. Please grant me admin rights."
                    )
        except UserNotParticipant:
            # Ignore if the user is not a participant
            continue
