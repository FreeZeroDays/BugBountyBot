import discord
import subprocess  # Import subprocess module
import os
import asyncio
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

def run_monitor():
    script_path = os.path.abspath("monitor.py")
    subprocess.Popen(["python3", script_path])

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Run the monitor.py script as a subprocess
    run_monitor()

    await asyncio.sleep(1800)  # Wait for a second before starting the file watchers
    bot.loop.create_task(file_watcher(config.DIRECTORY_PATH, config.CHANNEL_ID))
    bot.loop.create_task(file_watcher(config.OTHER_DIRECTORY_PATH, config.OTHER_CHANNEL_ID))

@bot.command()
async def run(ctx, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            await ctx.send(f'Content of {file_path}:\n```{file_content}```')
    except FileNotFoundError:
        await ctx.send(f'File {file_path} not found.')

async def process_file_change(file_path, channel_id, processed_files):
    base_name, file_ext = os.path.splitext(os.path.basename(file_path))
    if file_ext == '':
        return  # Ignore dot files

    with open(file_path, 'r', encoding='utf-8') as file:
        new_lines = file.readlines()
        if file_path in processed_files:
            previous_lines = processed_files[file_path]
            unique_lines = [line for line in new_lines if line not in previous_lines]
            if len(unique_lines) == 0:
                return
            processed_files[file_path].extend(unique_lines)
        else:
            processed_files[file_path] = new_lines
            return  # Skip processing for the first time
        channel = bot.get_channel(channel_id)
        message = f'New data in {file_path}:\n```' + ''.join(unique_lines) + '```'
        await asyncio.sleep(1)  # Add a small delay before sending the message
        await channel.send(message)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.processed_files = {}

    def on_modified(self, event):
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            asyncio.run_coroutine_threadsafe(process_file_change(file_path, self.channel_id, self.processed_files), bot.loop)

async def file_watcher(directory_path, channel_id):
    event_handler = FileChangeHandler(channel_id)
    observer = Observer()
    observer.schedule(event_handler, path=directory_path, recursive=True)
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        observer.stop()
        observer.join()

bot.run(config.TOKEN)
