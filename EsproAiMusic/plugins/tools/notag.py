from pyrogram import Client, filters
from EsproAiMusic import app

# Yeh function message ko delete karega agar username @HaiwanOwner tag hota hai
@app.on_message(filters.group)
async def delete_tagged_message(client, message):
    if message.entities:  # Check if there are any entities like mentions
        for entity in message.entities:
            if entity.type == "mention" and message.text[entity.offset:entity.offset + entity.length] == "@HaiwanOwner":
                await message.delete()  # Delete the message if @HaiwanOwner is tagged
                break

