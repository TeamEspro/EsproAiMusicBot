import random
import asyncio
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters

def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {cookie_txt_file}\n')
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""


# Global variable to track playback status
playing = False  
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID

def fetch_shorts_from_channel(channel_name):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        shorts_url = f"https://www.youtube.com/@{channel_name}"  # Channel URL
        info = ydl.extract_info(shorts_url, download=False)
        
        # Collect Shorts videos
        videos = [f"https://youtube.com/watch?v={video['id']}" for video in info['entries'] if 'Shorts' in video.get('title', '')]

        return videos

@app.on_message(filters.command("sritik") & filters.chat(ALLOWED_GROUP_ID))
async def play_shorts(client, message):
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

    playing = True
    await message.reply(f"Starting to play Shorts from {channel_name}. Use /stop to end playback.")

    # Join the voice chat before starting playback
    await join_voice_chat(message.chat.id)

    # Play each video one by one
    for video_url in videos:
        audio_info = yt_dlp.YoutubeDL({'format': 'bestaudio/best'}).extract_info(video_url, download=False)
        audio_url = audio_info['formats'][0]['url']
        await message.reply(f"Playing video: {video_url}")
        await play_audio_in_voice_chat(message.chat.id, audio_url)

    playing = False  # Reset playing status after all videos are played
    await leave_voice_chat(message.chat.id)  # Leave the voice chat after playback

async def join_voice_chat(chat_id):
    # Implement logic to join voice chat
    await app.join_voice_chat(chat_id)  # Replace with the correct method for joining voice chat

async def play_audio_in_voice_chat(chat_id, audio_url):
    # Implement your audio playback logic here
    await asyncio.sleep(10)  # Simulate audio playback duration (replace with actual logic)

async def stop_playback(client, message):
    global playing
    playing = False
    await message.reply("Stopped playback.")
    await leave_voice_chat(message.chat.id)  # Leave the voice chat when stopped

async def leave_voice_chat(chat_id):
    # Implement logic to leave voice chat
    await app.leave_voice_chat(chat_id)  # Replace with the correct method for leaving voice chat

@app.on_message(filters.command("stop") & filters.chat(ALLOWED_GROUP_ID))
async def handle_stop(client, message):
    await stop_playback(client, message)

