import random
import asyncio
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters



# Add your YouTube cookies here
cookies = """
# Paste your cookies here
"""

# Store the cookies in a file
with open("cookies.txt", "w") as f:
    f.write(cookies.strip())

# Global variable to track playback status
playing = False  

# Replace with your specific group ID or username
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID

def fetch_random_shorts():
    # Set options for yt-dlp
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Replace with your channel URL to fetch Shorts
        shorts_url = "https://www.youtube.com/@YourChannelName"  # Change this to your channel

        # Extract video information
        info = ydl.extract_info(shorts_url, download=False)
        videos = [f"https://youtube.com/watch?v={video['id']}" for video in info['entries'] if 'Shorts' in video.get('title', '')]

        if not videos:
            return None, None

        video_url = random.choice(videos)
        audio_info = ydl.extract_info(video_url, download=False)
        audio_url = audio_info['formats'][0]['url']
        
        return audio_url, video_url

@app.on_message(filters.command("play_random_shorts") & filters.chat(ALLOWED_GROUP_ID))
async def play_random_shorts(client, message):
    global playing
    if playing:
        await message.reply("Already playing Shorts. Use /stop to stop the playback.")
        return

    playing = True
    await message.reply("Starting to play random Shorts. Use /stop to end playback.")

    # Loop to continuously play random Shorts
    while playing:
        audio_url, shorts_url = fetch_random_shorts()
        if not audio_url:
            await message.reply("No Shorts found or an error occurred.")
            break

        await message.reply(f"Playing random Shorts video: {shorts_url}")

        # Play the audio in the voice chat
        await play_audio_in_voice_chat(message.chat.id, audio_url)

async def play_audio_in_voice_chat(chat_id, audio_url):
    # This is a placeholder for your actual audio playback implementation
    # Simulate audio playback duration
    await asyncio.sleep(10)  # Replace with actual audio duration logic

async def stop_playback(client, message):
    global playing
    playing = False
    await message.reply("Stopped playback.")

@app.on_message(filters.command("stop") & filters.chat(ALLOWED_GROUP_ID))
async def handle_stop(client, message):
    await stop_playback(client, message)

  
