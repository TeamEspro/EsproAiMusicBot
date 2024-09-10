from EsproAiMusic import app
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions



# Function to check if a user's bio contains a link
def bio_contains_link(bio):
    return bio and ("http" in bio or "https" in bio)

@app.on_message(filters.new_chat_members)
async def restrict_on_join(client, message):
    chat_id = message.chat.id
    new_members = message.new_chat_members
    
    for member in new_members:
        user_id = member.id
        first_name = member.first_name
        try:
            user_details = await client.get_users(user_id)  # User's details fetch karte hain
            bio = user_details.bio  # User's bio
            
            # Agar bio me 'http' ya 'https' ho to restrict kar do
            if bio_contains_link(bio):
                await client.restrict_chat_member(
                    chat_id,
                    user_id,
                    ChatPermissions(can_send_messages=False)  # Restrict user from sending messages
                )
                await message.reply_text(f"{first_name} ko restrict kiya gaya bio me link hone ke karan.")
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.text & filters.group)
async def check_bio_and_restrict(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    try:
        # Get user's bio details
        user_details = await client.get_users(user_id)
        bio = user_details.bio  # User's bio
        
        # Check if bio contains a link
        if bio_contains_link(bio):
            await client.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=False)  # Restrict from sending messages
            )
            await message.reply_text(f"{first_name} ko restrict kiya gaya bio me link hone ke karan.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.regex(r"(http|https)"))
async def restrict_on_link_message(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    try:
        # User ko restrict karte hain agar message me link ho
        await client.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(can_send_messages=False)  # Restrict user from sending messages
        )
        await message.reply_text(f"{first_name} ko restrict kiya gaya message me link bhejne ke karan.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# Run the bot
app.run()
