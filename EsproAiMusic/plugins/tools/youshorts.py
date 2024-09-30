import random
import asyncio
import yt_dlp
from EsproAiMusic import app
from pyrogram import Client, filters

playing = False
ALLOWED_GROUP_ID = -1002030185823  # Replace with your group ID

# Path to your YouTube cookies file
COOKIES_FILE = '
# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

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
.youtube.com	TRUE	/	TRUE	1756599123	__Secure-3PSIDCC	AKEyXzXj-b0QHfPnjPH_wcbOwn6rT2-VXrNV-9RE1brKj6xWTffYTzP7ktkJwOLi0YpLyUly'  # Replace with the path to your cookies.txt file

def fetch_shorts_from_channel(channel_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': COOKIES_FILE,  # Adding cookie file for authentication
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
    }

    # Get the channel's ID using the channel name
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'cookiefile': COOKIES_FILE}) as ydl:
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
