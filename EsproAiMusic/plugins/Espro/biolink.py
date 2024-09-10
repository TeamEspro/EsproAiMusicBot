from EsproAiMusic import app  # Ensure this import matches your actual setup
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# Define your group ID here
GROUP_ID = -1002030185823  # Replace with your actual group ID

@app.on_message(filters.new_chat_members)
async def on_new_member(client, message):
    new_member = message.new_chat_members[0]
    
    # Check if the new member has a bio
    if new_member.bio:
        # Check for links in the bio
        if "http" in new_member.bio or "https" in new_member.bio or ".com" in new_member.bio:
            # Restrict the new member
            await client.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=new_member.id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )
            await message.chat.send_message(
                text=f"{new_member.mention} has been restricted due to containing a link in their bio."
            )

@app.on_message(filters.text & filters.chat(GROUP_ID))
async def on_message(client, message):
    # Check for links in any message sent
    if "http" in message.text or "https" in message.text or ".com" in message.text:
        await client.restrict_chat_member(
            chat_id=GROUP_ID,
            user_id=message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )
        )
        await message.reply_text("You are restricted due to containing a link in your message.")


