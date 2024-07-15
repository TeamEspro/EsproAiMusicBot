import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from EsproAiMusic import app

#--------------------------

MUST_JOIN = "EsproUpdate"
#------------------------

Espro_PICS = [
"https://telegra.ph/file/2e85d11aefdf6cd01301b.jpg",
"https://telegra.ph/file/0a08b180583f13952336a.jpg",
"https://telegra.ph/file/ace92d59d19127d2d4e89.jpg",
"https://telegra.ph/file/bb0a28259990c6a978985.jpg",
"https://telegra.ph/file/ace92d59d19127d2d4e89.jpg",
"https://telegra.ph/file/a0db46dfacd94e489117b.jpg",
"https://telegra.ph/file/cd77be2595cdc2fca60a3.jpg",
"https://telegra.ph/file/632724b3d30c691247c77.jpg",
"https://telegra.ph/file/a2d01afe4f2cb1d4b650c.jpg",
"https://telegra.ph/file/94dc035df11dfb159b999.jpg",
"https://telegra.ph/file/fed9a5b1cbaaefc3a818c.jpg",
"https://telegra.ph/file/66fd03632cbb38bdb4193.jpg"

]
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    random.choice(Espro_PICS),
                    caption=f"๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ʏᴇᴛ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ ! ",)
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("๏Jᴏɪɴ๏", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛ ๏: {MUST_JOIN} !")
