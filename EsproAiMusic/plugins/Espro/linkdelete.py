from EsproAiMusic import app
from pyrogram import Client, filters
import re


# Link detection ke liye function
def is_link(message_text):
    url_pattern = r"(https?://[^\s]+|www\.[^\s]+)"  # URL detect karne ka pattern
    return re.search(url_pattern, message_text) is not None

# Message handler jo group me aaye har message ko check karega
@app.on_message(filters.group)
def link_checker(client, message):
    print(f"Received message: {message.text}")  # Debug statement
    
    if message.text and is_link(message.text):
        try:
            # Agar message me link hai to usse delete karo
            message.delete()
            print(f"Deleted a message containing link from {message.from_user.first_name}")
        except Exception as e:
            print(f"Failed to delete message: {e}")
    else:
        print("No link detected in the message.")  # Debug statement

# Bot ko start karne ke liye
app.run()
