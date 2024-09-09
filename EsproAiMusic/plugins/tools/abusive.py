from pyrogram import Client, filters
from pyrogram.types import Message
import re

# Initialize the Pyrogram client
app = Client("my_bot")

# List of abusive words (initialized empty, will be managed by bot commands)
ABUSIVE_WORDS = []

# Compile the abusive words into a regex pattern
def compile_pattern():
    return re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in ABUSIVE_WORDS) + r')\b', re.IGNORECASE)

pattern = compile_pattern()

@app.on_message(filters.text & filters.group)
async def filter_abuse(client: Client, message: Message):
    # Check if the message contains any abusive words
    if pattern.search(message.text):
        try:
            # Delete the message if it contains abusive content
            await message.delete()
        except Exception as e:
            print(f"An error occurred: {e}")

@app.on_message(filters.command("addabusive") & filters.user("YOUR_ADMIN_ID"))
async def add_abusive_word(client: Client, message: Message):
    # Extract the word to be added
    if len(message.command) < 2:
        return await message.reply_text("Usage: /addabusive <word>")
    
    word = message.text.split(None, 1)[1].strip().lower()
    
    if word in ABUSIVE_WORDS:
        return await message.reply_text(f"Word '{word}' is already in the list.")
    
    ABUSIVE_WORDS.append(word)
    global pattern
    pattern = compile_pattern()  # Recompile the pattern with the updated list
    await message.reply_text(f"Word '{word}' added to the list of abusive words.")

@app.on_message(filters.command("removeabusive") & filters.user("YOUR_ADMIN_ID"))
async def remove_abusive_word(client: Client, message: Message):
    # Extract the word to be removed
    if len(message.command) < 2:
        return await message.reply_text("Usage: /removeabusive <word>")
    
    word = message.text.split(None, 1)[1].strip().lower()
    
    if word not in ABUSIVE_WORDS:
        return await message.reply_text(f"Word '{word}' is not in the list.")
    
    ABUSIVE_WORDS.remove(word)
    global pattern
    pattern = compile_pattern()  # Recompile the pattern with the updated list
    await message.reply_text(f"Word '{word}' removed from the list of abusive words.")

# Start the client
app.run()
