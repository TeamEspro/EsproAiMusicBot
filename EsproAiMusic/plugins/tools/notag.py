from pyrogram import Client, filters
from pyrogram.types import Message
from EsproAiMusic import app





# Usernames ko store karne ke liye ek list
protected_usernames = ["@HaiwanOwner"]

# Command to add a username to the protected list
@app.on_message(filters.command("adduser") & filters.user("your_username"))  # Replace with your admin username
def add_user(client, message):
    if len(message.command) > 1:
        username = message.command[1].strip("@")  # Command format: /adduser @username
        if username not in protected_usernames:
            protected_usernames.append(username)
            message.reply_text(f"Username @{username} ko successfully add kar diya gaya hai.")
        else:
            message.reply_text(f"Username @{username} pehle se list mein hai.")
    else:
        message.reply_text("Please ek username provide karein. Format: /adduser @username")

# Check if the mentioned username is in the protected list
@app.on_message(filters.mentioned)
def delete_message(client, message):
    mentioned_usernames = [user.username for user in message.entities if user.type == "mention"]
    
    for username in mentioned_usernames:
        if username in protected_usernames and message.from_user.username != username:
            message.delete()  # Delete the message if username is in the protected list
            print(f"Deleted message from {message.from_user.first_name} mentioning @{username}")
            break

