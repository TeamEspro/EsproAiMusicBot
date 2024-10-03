from pyrogram import Client, filters
from pyrogram.types import Message
from EsproAiMusic import app



# List of approved user IDs who are allowed to tag
approved_user_ids = set()

# The username that no one should be able to tag without approval
TARGET_USERNAME = "haiwanowner"  # Replace with the username that shouldn't be tagged




# Command to approve a user by Telegram ID
@app.on_message(filters.command("approve") & filters.user("your_username"))
def approve_user(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            approved_user_ids.add(user_id)
            message.reply_text(f"User with ID {user_id} has been approved to tag @{TARGET_USERNAME}!")
        except ValueError:
            message.reply_text("Please provide a valid Telegram user ID!")
    else:
        message.reply_text("Please provide the Telegram user ID to approve.")


# Monitor group messages and delete if someone tags the target username without approval
@app.on_message(filters.group)
def monitor_messages(client: Client, message: Message):
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention" and entity.user and entity.user.username == TARGET_USERNAME:
                if message.from_user.id not in approved_user_ids:
                    message.delete()
                    client.send_message(
                        message.chat.id, 
                        f"Sorry {message.from_user.mention}, you're not allowed to tag @{TARGET_USERNAME}."
                    )


