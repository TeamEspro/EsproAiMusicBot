import random
import asyncio
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters

import os
import glob
import random
import logging

def COOKIES_FILE():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {COOKIES_FILE}\n')
    return f"""cookies/{str(COOKIES_FILE).split("/")[-1]}"""

playing = False
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID



def fetch_shorts_from_channel(channel_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': COOKIES_FILE(),  # Corrected cookie usage
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
    }

    try:
        # Get the channel ID from the channel name
        with yt_dlp.YoutubeDL({'quiet': True, 'cookiefile': COOKIES_FILE()}) as ydl:
            channel_info = ydl.extract_info(f"https://www.youtube.com/@{channel_name}", download=False)
            channel_id = channel_info['id']
    except Exception as e:
        print(f"Error fetching channel ID: {e}")
        return []

    # Fetch all videos from the channel
    search_url = f"https://www.youtube.com/channel/{channel_id}/videos"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            # Filter videos that are less than 60 seconds (Shorts criteria)
            shorts_videos = [
                f"https://youtube.com/watch?v={entry['id']}"
                for entry in info['entries'] if entry.get('duration') and entry['duration'] < 60
            ]
            return shorts_videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []



@app.on_message(filters.command("Rritik") & filters.chat(ALLOWED_GROUP_ID))
async def play_random_short(client, message):
    global playing

    # Delete the command message sent by the user
    await message.delete()

    if playing:
        wait_message = await message.reply("Already playing Shorts. Use /stop to stop the playback.")
        await asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
        await wait_message.delete()
        return

    command_parts = message.command
    if len(command_parts) < 2:
        error_message = await message.reply("Please provide a channel name after the command.")
        await asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
        await error_message.delete()
        return

    # Send a "please wait" message to the user
    wait_message = await message.reply("Fetching Shorts, please wait...")

    channel_name = command_parts[1]  # Get the channel name from command
    videos = fetch_shorts_from_channel(channel_name)

    # Delete the "please wait" message after fetching the videos
    await wait_message.delete()

    if not videos:
        error_message = await message.reply("No Shorts found for the specified channel.")
        await asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
        await error_message.delete()
        return

    # Select a random video from the list
    random_video_url = random.choice(videos)
    audio_info = yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'cookiefile': COOKIES_FILE}).extract_info(random_video_url, download=False)
    audio_url = audio_info['formats'][0]['url']

    playing = True
    success_message = await message.reply(f"Playing a random short from {channel_name}: {random_video_url}")

    # Delete the success message after 10 seconds
    await asyncio.sleep(10)
    await success_message.delete()

    # Join the voice chat and play the audio
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
        error_message = await message.reply("No audio is currently playing.")
        await asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
        await error_message.delete()
        return

    playing = False
    stop_message = await message.reply("Stopped playback.")
    await asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
    await stop_message.delete()
