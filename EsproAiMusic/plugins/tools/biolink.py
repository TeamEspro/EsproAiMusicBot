import re
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated
from EsproAiMusic import app

# Regular expression to match a URL in the bio
URL_PATTERN = r"(https?://[^\s]+)"

# Function to mute the user
async def mute_user(chat_id: int, user_id: int):
    try:
        await app.restrict_chat_member(chat_id, user_id, permissions={"can_send_messages": False})
        print(f"User {user_id} has been muted for adding a link in their bio.")
    except Exception as e:
        print(f"Error muting user {user_id}: {e}")

# Function to delete a message
async def delete_message(chat_id: int, message_id: int):
    try:
        await app.delete_messages(chat_id, message_ids=[message_id])
        print(f"Message {message_id} has been deleted.")
    except Exception as e:
        print(f"Error deleting message {message_id}: {e}")

# Event handler to monitor profile changes
@app.on_chat_member_updated(filters.group)
async def check_bio_for_link(client: app, member: ChatMemberUpdated):
    # Ensure new_chat_member and old_chat_member exist
    if member.old_chat_member and member.new_chat_member:
        new_user = member.new_chat_member.user
        old_user = member.old_chat_member.user

        # Ensure that the user object exists and compare their IDs
        if new_user and old_user and new_user.id == old_user.id:
            try:
                # Get the full user information to access the bio
                full_user_info = await app.get_users(new_user.id)

                # Extract the user's bio (it's called `description` in get_users)
                new_bio = full_user_info.bio  # This now retrieves the bio properly

                if new_bio:
                    # Check if the new bio contains a URL
                    if re.search(URL_PATTERN, new_bio):
                        # Mute the user in the group
                        await mute_user(member.chat.id, new_user.id)

                        # Delete the message if applicable (you can adjust this based on your use case)
                        async for message in app.search_messages(chat_id=member.chat.id, from_user=new_user.id, limit=1):
                            await delete_message(member.chat.id, message.message_id)

                        # Send a message informing that the user has been muted and their message deleted
                        await client.send_message(
                            chat_id=member.chat.id,
                            text=f"User {new_user.mention} has been muted for having a link in their bio, and their message has been deleted."
                        )

            except Exception as e:
                print(f"Error fetching user bio: {e}")
