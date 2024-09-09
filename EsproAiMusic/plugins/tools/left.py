import asyncio
from EsproAiMusic import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont

# Helper functions for font and text resize
get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# Function to generate user info image
async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

# Background and font path
bg_path = "EsproAiMusic/assets/userinfo.png"
font_path = "EsproAiMusic/assets/hiroko.ttf"

# In-memory dictionary to store feature state
feature_state = {}

# Command to enable or disable the left message feature
@app.on_message(filters.command("leftmsg") & filters.group)
async def toggle_left_message(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /leftmsg [on|off]")
        return

    state = message.command[1].strip().lower()
    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        if state == "on":
            feature_state[chat_id] = True
            await message.reply_text(f"Left message feature enabled for {message.chat.title}")
        elif state == "off":
            feature_state[chat_id] = True
            await message.reply_text(f"Left message feature disabled for {message.chat.title}")
        else:
            await message.reply_text("Usage: /leftmsg [on|off]")
    else:
        await message.reply("Only admins can use this command.")

# Event handler when a member leaves the chat
@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):
    chat_id = member.chat.id

    # Check if the feature is enabled for this chat
    if not feature_state.get(chat_id, False):
        return

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "left", "restricted"}
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    # Check if the user has a profile photo
    if user.photo and user.photo.big_file_id:
        try:
            # Download the user's profile photo
            photo = await app.download_media(user.photo.big_file_id)

            # Generate user info image
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            # Create the caption and button
            caption = f"**#New_Member_Left**\n\n**๏** {user.mention} **ʜᴀs ʟᴇғᴛ ᴛʜɪs ɢʀᴏᴜᴘ**\n**๏ sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
            button_text = "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏"
            deep_link = f"tg://openmessage?user_id={user.id}"

            # Send the message with photo, caption, and button
            message = await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)]
                ])
            )

            # Wait for 1 second
            await asyncio.sleep(1)

            # Delete the message after 1 second
            await client.delete_messages(chat_id=member.chat.id, message_ids=message.message_id)

        except RPCError as e:
            print(f"RPCError occurred: {e}")
            return
    else:
        # Handle the case where the user has no profile photo
        print(f"User {user.id} has no profile photo.")
