import asyncio
from EsproAiMusic import app
from pyrogram import filters
from pyrogram.errors import RPCError
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

# Event handler when a member leaves the chat
@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

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

            # Check if the message has a message_id
            if message and message.message_id:
                # Wait for 10 seconds
                await asyncio.sleep(10)
                
                # Delete the message after 10 seconds
                await client.delete_messages(chat_id=member.chat.id, message_ids=message.message_id)
            else:
                print("The sent message does not have a message_id attribute.")
        
        except RPCError as e:
            print(f"RPCError occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        # Handle the case where the user has no profile photo
        print(f"User {user.id} has no profile photo.")
