
from EsproAiMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall
import yt_dlp  # To search and download YouTube URLs


pytgcalls = PyTgCalls(app)

# Banned users list (if needed)
BANNED_USERS = []

# Function to search and get the URL of the song from YouTube using yt-dlp
def get_youtube_url(song_name):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries']
            return results[0]['url'] if results else None
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return None

# Command to play song in a remote group or channel
@app.on_message(filters.command("play_remote") & filters.group & ~filters.user(BANNED_USERS))
async def play_remote_song(client: Client, message: Message):
    # Command should be: /play_remote <group_or_channel_id> <song_name>
    if len(message.command) < 3:
        await message.reply("Usage: /play_remote <group_or_channel_id> <song_name>")
        return

    target_chat_id = message.command[1]  # Target group or channel ID
    song_name = " ".join(message.command[2:])  # Song name from the command

    # Get YouTube URL using the song name
    song_url = get_youtube_url(song_name)
    
    if not song_url:
        await message.reply("Song not found!")
        return

    try:
        # Join the group call of the target group/channel
        await pytgcalls.join_group_call(target_chat_id)
        
        # Stream the song in the target group/channel
        await pytgcalls.start_stream(target_chat_id, song_url)
        
        await message.reply(f"Playing '{song_name}' in group/channel: {target_chat_id}")
    except NoActiveGroupCall:
        await message.reply("No active group call in the target group/channel.")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Error handling for when the stream ends
@pytgcalls.on_stream_end()
async def on_stream_end(update):
    chat_id = update.chat_id
    await app.send_message(chat_id, "Stream has ended.")
    print(f"Stream ended in {chat_id}")

# Start the bot
pytgcalls.run()
