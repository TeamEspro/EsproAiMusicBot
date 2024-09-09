from pyrogram import filters
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pyrogram.types import ChatPermissions
import re
from EsproAiMusic import app

# Regex pattern to detect URLs/links in the bio
url_pattern = re.compile(r"(https?://[^\s]+|www\.[^\s]+)")

# Function to restrict new members if they have links in their bio
@app.on_message(filters.new_chat_members)
async def auto_restrict_new_member(_, message):
    new_members = message.new_chat_members
    chat_id = message.chat.id

    for new_member in new_members:
        user_id = new_member.id
        try:
            # Fetch user details
            user = await app.get_users(user_id)

            # Check the bio for links
            if user.bio and url_pattern.search(user.bio):
                # If the bio contains a link, restrict the member
                try:
                    await app.restrict_chat_member(
                        chat_id,
                        user_id,
                        ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_send_polls=False
                        )  # Restrict the member
                    )
                    await message.reply_text(f"🚫 {user.first_name} has been restricted because their bio contains a link.")
                except ChatAdminRequired:
                    await message.reply_text(
                        "⚠️ I need admin rights with 'Restrict Members' permission to restrict users. Please grant me admin rights."
                    )
        except UserNotParticipant:
            continue

# Function to restrict a member if they send a message and have a link in their bio
@app.on_message(filters.group)
async def auto_restrict_message(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        # Fetch user details
        user = await app.get_users(user_id)

        # Check the bio for links
        if user.bio and url_pattern.search(user.bio):
            # If the bio contains a link, restrict the member
            try:
                await app.restrict_chat_member(
                    chat_id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_other_messages=False,
                        can_send_polls=False
                    )  # Restrict the member
                )
                await message.reply_text(f"🚫 {user.first_name} has been restricted because their bio contains a link.")
            except ChatAdminRequired:
                await message.reply_text(
                    "⚠️ I need admin rights with 'Restrict Members' permission to restrict users. Please grant me admin rights."
                )
    except UserNotParticipant:
        return
