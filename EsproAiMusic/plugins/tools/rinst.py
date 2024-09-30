import os
import time
from EsproAiMusic import app
from pyrogram import Client, filters

# Folder where reels are downloaded
REELS_FOLDER = "./profile_name"
reel_files = os.listdir(REELS_FOLDER)
current_reel_index = 0

# Function to play the next reel
def play_next_reel(client, message):
    global current_reel_index

    # If we've played all reels, start from the beginning
    while True:
        if current_reel_index >= len(reel_files):
            current_reel_index = 0  # Loop back to the first reel if all have been played

        reel_file = os.path.join(REELS_FOLDER, reel_files[current_reel_index])
        current_reel_index += 1

        try:
            # Attempt to send the reel video
            client.send_video(chat_id=message.chat.id, video=reel_file)
            
            # Assuming each reel is about 30 seconds long
            time.sleep(30)  # You can customize this based on actual reel length
        except Exception as e:
            # If there's an error, print it and skip to the next reel
            print(f"Error playing reel {reel_file}: {e}")
            continue  # Go to the next reel

        # Check if stop command is received
        if stop_command_received:
            break

# Start playing reels
@app.on_message(filters.command("start_reels"))
def start_reels(client, message):
    global stop_command_received
    stop_command_received = False
    play_next_reel(client, message)

# Stop playing reels
@app.on_message(filters.command("stop_reels"))
def stop_reels(client, message):
    global stop_command_received
    stop_command_received = True
    client.send_message(chat_id=message.chat.id, text="Reels playback stopped.")


stop_command_received = False

