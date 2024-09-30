import os
import time
from EsproAiMusic import app
from pyrogram import Client, filters
import asyncio
import aiohttp

# Folder where reels are downloaded
REELS_FOLDER = "./profile_name"

# Create the folder if it doesn't exist
if not os.path.exists(REELS_FOLDER):
    os.makedirs(REELS_FOLDER)
    print(f"Folder '{REELS_FOLDER}' created.")

# Initialize global variables
reel_files = os.listdir(REELS_FOLDER)
current_reel_index = 0
stop_command_received = False
session = None

# Function to play the next reel
async def play_next_reel(client, message):
    global current_reel_index, session

    # Ensure aiohttp session is created
    if session is None:
        session = aiohttp.ClientSession()

    # If we've played all reels, start from the beginning
    while True:
        if current_reel_index >= len(reel_files):
            current_reel_index = 0  # Loop back to the first reel if all have been played

        reel_file = os.path.join(REELS_FOLDER, reel_files[current_reel_index])
        current_reel_index += 1

        try:
            # Attempt to send the reel video
            await client.send_video(chat_id=message.chat.id, video=reel_file)
            
            # Assuming each reel is about 30 seconds long
            await asyncio.sleep(30)  # You can customize this based on actual reel length
        except Exception as e:
            # If there's an error, print it and skip to the next reel
            print(f"Error playing reel {reel_file}: {e}")
            continue  # Go to the next reel

        # Check if stop command is received
        if stop_command_received:
            break

# Start playing reels
@app.on_message(filters.command("start_reels"))
async def start_reels(client, message):
    global stop_command_received
    stop_command_received = False
    await play_next_reel(client, message)

# Stop playing reels
@app.on_message(filters.command("stop_reels"))
async def stop_reels(client, message):
    global stop_command_received
    stop_command_received = True
    await client.send_message(chat_id=message.chat.id, text="Reels playback stopped.")

# Close aiohttp session on shutdown
@app.on_disconnect
async def close_session():
    global session
    if session:
        await session.close()  # Close the aiohttp session
        session = None
        print("Client session closed.")

# Initialize the bot and handle session cleanup
try:
    app.run()  # Start the bot
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure aiohttp session is closed on exit
    if session:
        asyncio.run(close_session())
