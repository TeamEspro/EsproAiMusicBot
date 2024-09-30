import random
import asyncio
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters

# Add your YouTube cookies here
cookies = """
.youtube.com	TRUE	/	TRUE	1725064696	GPS	1
.youtube.com	TRUE	/	TRUE	1759623036	PREF	f6=40000000&tz=Asia.Calcutta
.youtube.com	TRUE	/	TRUE	1756598959	__Secure-1PSIDTS	sidts-CjEBUFGoh9IhlUfsa8o-f__YyEWRWsPZudufp3LOws98lASWtElXKOEsulYBOa7GJ9ESEAA
.youtube.com	TRUE	/	TRUE	1756598959	__Secure-3PSIDTS	sidts-CjEBUFGoh9IhlUfsa8o-f__YyEWRWsPZudufp3LOws98lASWtElXKOEsulYBOa7GJ9ESEAA
.youtube.com	TRUE	/	FALSE	1759622959	HSID	ABSR9EKYytAYvmSL8
.youtube.com	TRUE	/	TRUE	1759622959	SSID	A7N1hORIzRyntmy2A
.youtube.com	TRUE	/	FALSE	1759622959	APISID	QJWf1u2cD4wwia5m/Ai69xpjnt0IVmqtJ6
.youtube.com	TRUE	/	TRUE	1759622959	SAPISID	rnlHL_ltWKRft7hX/Ai2pH7pAxHTKoDukO
.youtube.com	TRUE	/	TRUE	1759622959	__Secure-1PAPISID	rnlHL_ltWKRft7hX/Ai2pH7pAxHTKoDukO
.youtube.com	TRUE	/	TRUE	1759622959	__Secure-3PAPISID	rnlHL_ltWKRft7hX/Ai2pH7pAxHTKoDukO
.youtube.com	TRUE	/	FALSE	1759622959	SID	g.a000ngiKLdHdQcXnXFIoNrENmwHLDoCJOf4EYKg0ycHGsVhtdHqe7NO19GtNMaGO5wh90feH9wACgYKASASARISFQHGX2Miq4SEe2PECwP9kkNNUtc6BxoVAUF8yKpS2zBN5Y1DokitNWJxN2QU0076
.youtube.com	TRUE	/	TRUE	1759622959	__Secure-1PSID	g.a000ngiKLdHdQcXnXFIoNrENmwHLDoCJOf4EYKg0ycHGsVhtdHqeoGXSErIBfQXDVsEHLkV1oQACgYKAaYSARISFQHGX2MiuAa6QXE6pclK9jk_6owvEBoVAUF8yKpx5m5mi6FZyrTytHccX_Kt0076
.youtube.com	TRUE	/	TRUE	1759622959	__Secure-3PSID	g.a000ngiKLdHdQcXnXFIoNrENmwHLDoCJOf4EYKg0ycHGsVhtdHqeMZ9hB3ZtZ02KhcR-pAFX0gACgYKAU0SARISFQHGX2MiLgICxBZRRkwR9BFzqSe70xoVAUF8yKoWHxRzKOI0TI_4zw38P3H60076
.youtube.com	TRUE	/	TRUE	1759622960	LOGIN_INFO	AFmmF2swRQIhAJLgeIus_m4t44MaaG4gi-ltDl9A_TMc4_edSdUtrV6WAiAfqwBJz1_WKApLrkm1EVi87xLJT9Qj3b_nOXLlRsUmUA:QUQ3MjNmd1pTbEt2R0NQUUJjU2NrTXZLc1dMYi1nRXM0WmxNMWlIUWFFYW1tcGxLMWZWMW9TZWh1dnoyMko4WHQ4R0wzR09ndmdGRlB3QlMxbnhuMTJ5MFJ0VzRCTkFtWnpnU2JvY2Y4MG9ZUGs5UzVuZEtENl8xQTlRQkk4dkR6bXlvSFI3Vm9HcUlDZ3IwbXR4T1RzOUFTNUQ2VjJOS0NB
.youtube.com	TRUE	/	TRUE	1725063645	CONSISTENCY	AKreu9uzcDtuwe_2xGqxBXMGdsOjzImbx_wKj-fMcQ8hT6khKriGE6oVxgAIPNcqxh32nYhKUS1Ma-YnaNWIfVmqKQlibGq0pgrIech8bm1cqiQ7BmSUiz_YXDI
.youtube.com	TRUE	/	FALSE	1756599123	SIDCC	AKEyXzW8mbs0P01S32qzI9GnyO47jQJ6Ds0c-0kNCvmyUO4CrvvWjGFkuAghs04CAZ0uIzVL
.youtube.com	TRUE	/	TRUE	1756599123	__Secure-1PSIDCC	AKEyXzXpg94HRdAT_433RDYgC9sguKWgbft74HIo3M_vfMb5Yz6326gi7xZzRpN6f9SmIgkrbg
.youtube.com	TRUE	/	TRUE	1756599123	__Secure-3PSIDCC	AKEyXzXj-b0QHfPnjPH_wcbOwn6rT2-VXrNV-9RE1brKj6xWTffYTzP7ktkJwOLi0YpLyUly
"""

# Store the cookies in a file
with open("cookies.txt", "w") as f:
    f.write(cookies.strip())

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

@app.on_message(filters.command("play_shorts") & filters.chat(ALLOWED_GROUP_ID))
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

