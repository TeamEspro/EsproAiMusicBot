from pyrogram import Client, filters
from EsproAiMusic import app
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio


pytg = PyTgCalls(app)

@app.on_message(filters.command("playsong", prefixes="!") & filters.group)
async def play_song(client: Client, message: Message):
    if len(message.command) < 3:
        await message.reply("Command ka format galat hai. Sahi format: !playsong <channel_id> <audio_file_path>")
        return
    
    # Aapka channel ya group jisme song play karna hai
    group_or_channel_id = message.command[1]
    
    # Song ka path
    song_path = message.command[2]

    try:
        await pytg.join_group_call(
            group_or_channel_id,
            InputAudioStream(
                song_path,
                HighQualityAudio()  # High Quality Audio stream use kar rahe hain
            )
        )
        await message.reply(f"Song successfully play ho gaya {group_or_channel_id} mein.")
    
    except Exception as e:
        await message.reply(f"Kuch galat ho gaya: {e}")

@app.on_message(filters.command("stop", prefixes="!") & filters.group)
async def stop_song(client: Client, message: Message):
    group_or_channel_id = message.command[1]

    try:
        await pytg.leave_group_call(group_or_channel_id)
        await message.reply(f"Music stop kar diya {group_or_channel_id} mein.")
    except Exception as e:
        await message.reply(f"Kuch galat ho gaya: {e}")

# Bot ko start kijiye

pytg.start()
print("Bot is running...")

# To stop the bot:
app.idle()
