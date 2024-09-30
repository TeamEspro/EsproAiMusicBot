import random
import asyncio
import os
import glob
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters

def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(os.path.join(folder_path, 'logs.csv'), 'a') as file:
        file.write(f'Chosen File: {cookie_txt_file}\n')
    return f"{folder_path}/{os.path.basename(cookie_txt_file)}"

playing = False
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID

def fetch_shorts_from_channel(channel_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': cookie_txt_file(),  # Use the cookies file here
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
    }

    # Get the channel's ID using the channel name
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            channel_info = ydl.extract_info(f"https://www.youtube.com/@{channel_name}", download=False)
            channel_id = channel_info['id']  # Extract the channel ID
    except Exception as e:
        print(f"Error fetching channel ID: {e}")
        return []

    # Now use the channel ID to get the Shorts
    shorts_url = f"https://www.youtube.com/channel/{channel_id}/shorts"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(shorts_url, download=False)
            # Collect all Shorts videos
            videos = [f"https://youtube.com/watch?v={entry['id']}" for entry in info['entries'] if 'Shorts' in entry.get('title', '')]
            return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []



@app.on_message(filters.command("Rritik") & filters.chat(ALLOWED_GROUP_ID))
async def play_random_short(client, message):
    global playing
    if playing:
        await message.reply("Already playing Shorts. Use /stop to stop the playback.")
        return

    command_parts = message.command
    if len(command_parts) < 2:
        await message.reply("Please provide a channel name after the command.")
        return

    channel_name = command_parts[1]  # Get the channel name from command
    videos = fetch_shorts_from_channel(channel_name)

    if not videos:
        await message.reply("No Shorts found for the specified channel.")
        return

    # Select a random video from the list
    random_video_url = random.choice(videos)
    audio_info = yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'cookiefile': cookie_txt_file()}).extract_info(random_video_url, download=False)
    audio_url = audio_info['formats'][0]['url']

    playing = True
    await message.reply(f"Playing a random short from {channel_name}: {random_video_url}")

    # Join the voice chat
    await join_voice_chat(message.chat.id)

    await play_audio_in_voice_chat(message.chat.id, audio_url)

    playing = False  # Reset playing status after the video is played

async def join_voice_chat(chat_id):
    # Logic to join the voice chat
    await app.join_voice_chat(chat_id)  # Make sure your bot has the required permissions

async def play_audio_in_voice_chat(chat_id, audio_url):
    # Placeholder for audio playback logic
    print(f"Now playing audio from: {audio_url}")
    await asyncio.sleep(10)  # Simulate audio playback duration; replace with actual playback logic.
    print(f"Finished playing audio from: {audio_url}")  # Replace with actual playback logic.

@app.on_message(filters.command("stop") & filters.chat(ALLOWED_GROUP_ID))
async def handle_stop(client, message):
    global playing
    if not playing:
        await message.reply("No audio is currently playing.")
        return

    playing = False
    await message.reply("Stopped playback.")

