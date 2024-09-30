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



playing = False
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID

def fetch_shorts_from_channel(channel_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # Use the cookies file here
    }

    shorts_url = f"https://www.youtube.com/@{channel_name}/shorts"  # URL for Shorts
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(shorts_url, download=False)
            # Collect Shorts videos
            videos = [f"https://youtube.com/watch?v={entry['id']}" for entry in info['entries'] if 'Shorts' in entry.get('title', '')]
            return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

@app.on_message(filters.command("play_all_shorts") & filters.chat(ALLOWED_GROUP_ID))
async def play_all_shorts(client, message):
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
    await message.reply(f"Starting to play all Shorts from {channel_name}. Use /stop to end playback.")

    for video_url in videos:
        audio_info = yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'cookiefile': 'cookies.txt'}).extract_info(video_url, download=False)
        audio_url = audio_info['formats'][0]['url']
        await message.reply(f"Playing video: {video_url}")

        await play_audio_in_voice_chat(message.chat.id, audio_url)

    playing = False  # Reset playing status after all videos are played

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
