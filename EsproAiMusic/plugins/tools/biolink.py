import re
import logging
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, Message

# Regular expression to match a URL in the bio or message
URL_PATTERN = r"(https?://[^\s]+)"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("my_bot")

# Function to mute the user
async def mute_user(chat_id: int, user_id: int):
    try:
        await app.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": True})
        logger.info(f"User {user_id} has been muted.")
    except RPCError as e:
        logger.error(f"Error muting user {user_id}: {e}")

# Function to delete a message
async def delete_message(chat_id: int, message_id: int):
    try:
        await app.delete_messages(chat_id, message_id)
        logger.info(f"Message {message_id} has been deleted.")
    except RPCError as e:
        logger.error(f"Error deleting message {message_id}: {e}")

# Event handler when a member joins the group
@app.on_chat_member_updated(filters.group)
async def member_joined(client: Client, member: ChatMemberUpdated):
    if member.new_chat_member and member.old_chat_member is None:
        user = member.new_chat_member.user
        if user:
            try:
                # Fetch the full user profile to get bio
                full_user_info = await app.get_users(user.id)
                new_bio = full_user_info.bio
                
                if new_bio and re.search(URL_PATTERN, new_bio):
                    # Mute the user if the bio contains a link
                    await mute_user(member.chat.id, user.id)
                    
                    # Send a notification to the group
                    await client.send_message(
                        chat_id=member.chat.id,
                        text=f"User {user.mention} has been muted for having a link in their bio."
                    )
            except Exception as e:
                logger.error(f"Error processing user bio for user {user.id}: {e}")

# Event handler for messages in the group
@app.on_message(filters.group)
async def message_handler(client: Client, message: Message):
    if message.from_user:
        user_id = message.from_user.id
        if re.search(URL_PATTERN, message.text or ''):
            try:
                # Mute the user if the message contains a link
                await mute_user(message.chat.id, user_id)
                
                # Delete the message
                await delete_message(message.chat.id, message.message_id)

                # Notify the group about the action taken
                await client.send_message(
                    chat_id=message.chat.id,
                    text=f"User {message.from_user.mention} has been muted for posting a link."
                )
            except Exception as e:
                logger.error(f"Error processing message from user {user_id}: {e}")

if __name__ == "__main__":
    app.run()
