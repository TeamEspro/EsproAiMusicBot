from EsproAiMusic import app
from pyrogram import filters
import re

# Define a URL pattern to detect links in the bio
URL_PATTERN = re.compile(r"(https?://[^\s]+|www\.[^\s]+)")

# Function to mute users if they have a link in their bio when they join the group
@app.on_chat_member_updated(filters.group)
async def check_bio_for_links(client, chat_member_update):
    new_member = chat_member_update.new_chat_member

    # Ensure that the user has joined the group
    if new_member.status == "member" and new_member.user:
        try:
            # Fetch the user information using get_chat (to get bio)
            user_info = await client.get_chat(new_member.user.id)
            bio = user_info.bio  # 'bio' holds the user's bio/about section

            # Check if their bio contains a link
            if bio and URL_PATTERN.search(bio):
                # Mute the user
                await client.restrict_chat_member(
                    chat_id=chat_member_update.chat.id,
                    user_id=new_member.user.id,
                    permissions={"can_send_messages": False},  # Mute the user
                )
                await client.send_message(
                    chat_id=chat_member_update.chat.id,
                    text=f"**{new_member.user.mention} has been muted** because their bio contains a link.",
                )
        except Exception as e:
            print(f"Failed to fetch bio or mute user: {e}")

# Function to check messages from users and mute them if they have a link in their bio
@app.on_message(filters.group & filters.text)
async def check_message_bio_for_links(client, message):
    user = message.from_user

    if user:
        try:
            # Fetch the user information using get_chat (to get bio)
            user_info = await client.get_chat(user.id)
            bio = user_info.bio  # 'bio' holds the user's bio/about section

            # Check if their bio contains a link
            if bio and URL_PATTERN.search(bio):
                # Mute the user
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user.id,
                    permissions={"can_send_messages": False},  # Mute the user
                )
                await client.send_message(
                    chat_id=message.chat.id,
                    text=f"**{user.mention} has been muted** because their bio contains a link.",
                )
        except Exception as e:
            print(f"Failed to fetch bio or mute user: {e}")
