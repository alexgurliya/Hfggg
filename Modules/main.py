import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
from bs4 import BeautifulSoup
import core as helper
import datetime
import master
import ffmpeg 

from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

API_ID    = os.environ.get("API_ID", "21705536")
API_HASH  = os.environ.get("API_HASH", "c5bb241f6e3ecf33fe68a444e288de2d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8020618163:AAEQTBjtfNsB7cMtx053fYFwJwIVfSjNVRk") 

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
  
import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/@ROWDXYBOT"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/@ROWDXYBOT"),
        ],
        [
            InlineKeyboardButton(text="📫 Updates Channel", url="https://t.me/+6rUIkO4lpZNlOTE1"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/@ROWDXYBOT"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/@ROWDXYBOT"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/+6rUIkO4lpZNlOTE1"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    "https://graph.org/file/48fd0f6213ace4ddcf834-12d6e97b142aef2fb0.jpg",
    # Add more image URLs as needed
]

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        "** Hey Bro 👋 !**\n\n"
        "➽ **I am powerful uploader bot 📥**\n\n"
        "➽ **I Can Extract Videos & Pdf From Your Text File and Upload to Telegram**\n\n"
        "➽ **For Help Use Command /Guide ⚔️**\n\n"
        "➽ **For Stop ⛔ working process ⇶ /stop Command**\n\n"
        "➽ **𝐔𝐬𝐞 /Rowdy Command To Download  Data From TXT File 🗃️ \n\n"
        "➽ **𝐌𝐚𝐝𝐞 𝐁𝐲: ᏒᎾᏯᎠᎽ 🦁 **"
    )

    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()


COOKIES_FILE_PATH = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")
ADMIN_ID = 7696342661 # Admin ID

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    """
    Command: /cookies
    Allows admin to upload or update a cookies file dynamically.
    """
    if m.from_user.id != ADMIN_ID:
        await m.reply_text("You are not authorized to use this command.")
        return

    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the admin to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        cookies_path = await input_message.download(file_name=COOKIES_FILE_PATH)
        await input_message.reply_text(
            f"✅ Cookies file has been successfully updated.\n📂 Saved at: `{COOKIES_FILE_PATH}`"
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")


# File paths
SUBSCRIPTION_FILE = "subscription_data.txt"
CHANNELS_FILE = "channels_data.json"

# Admin ID
YOUR_ADMIN_ID = 7696342661

# Function to read subscription data
def read_subscription_data():
    if not os.path.exists(SUBSCRIPTION_FILE):
        return []
    with open(SUBSCRIPTION_FILE, "r") as f:
        return [line.strip().split(",") for line in f.readlines()]


# Function to read channels data
def read_channels_data():
    if not os.path.exists(CHANNELS_FILE):
        return []
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)


# Function to write subscription data
def write_subscription_data(data):
    with open(SUBSCRIPTION_FILE, "w") as f:
        for user in data:
            f.write(",".join(user) + "\n")


# Function to write channels data
def write_channels_data(data):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Admin-only decorator
def admin_only(func):
    async def wrapper(client, message: Message):
        if message.from_user.id != YOUR_ADMIN_ID:
            await message.reply_text("You are not authorized to use this command.")
            return
        await func(client, message)
    return wrapper

# How to use:-
@bot.on_message(filters.command("Guide"))
async def guide_handler(client: Client, message: Message):
    guide_text = (
        "🔑 **How to get started with Premium**:\n\n"
        "1. **First of all**, contact the owner and buy a premium plan. 💰\n"
        "2. **If you are a premium user**, you can check your plan by using `/myplan`. 🔍\n\n"
        "📖 **Usage**:\n\n"
        "3. **🛡️Use command/adduser {id} expire date.\n"
        "1. `/add_channel -100{channel_id}` - Add a channel to the bot.\n"
        "2. `/remove_channel -100{channel_id}` - Remove a channel from the bot.\n"
        "3. `/rowdy .txt` file command - Process the .txt file.\n"
        "4. `/stop` - Stop the task running in the bot. 🚫\n\n"
        "If you have any questions, feel free to ask! 💬"
    )
    await message.reply_text(guide_text)

# 1. /adduser
@bot.on_message(filters.command("adduser") & filters.private)
@admin_only
async def add_user(client, message: Message):
    try:
        _, user_id, expiration_date = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data.append([user_id, expiration_date])
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} added with expiration date {expiration_date}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /adduser <user_id> <expiration_date>")


# 2. /removeuser
@bot.on_message(filters.command("removeuser") & filters.private)
@admin_only
async def remove_user(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data = [user for user in subscription_data if user[0] != user_id]
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} removed.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /removeuser <user_id>")

YOUR_ADMIN_ID = 7003164707

# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == YOUR_ADMIN_ID

# Command to show all users (Admin only)
@bot.on_message(filters.command("users") & filters.private)
async def show_users(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    subscription_data = read_subscription_data()
    
    if subscription_data:
        users_list = "\n".join(
            [f"{idx + 1}. User ID: `{user[0]}`, Expiration Date: `{user[1]}`" for idx, user in enumerate(subscription_data)]
        )
        await message.reply_text(f"**👥 Current Subscribed Users:**\n\n{users_list}")
    else:
        await message.reply_text("ℹ️ No users found in the subscription data.")

# 3. /myplan
@bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()  # Make sure this function is implemented elsewhere

    # Define YOUR_ADMIN_ID somewhere in your code
    if user_id == str(YOUR_ADMIN_ID):  # YOUR_ADMIN_ID should be an integer
        await message.reply_text("**✨ You have permanent access!**")
    elif any(user[0] == user_id for user in subscription_data):  # Assuming subscription_data is a list of [user_id, expiration_date]
        expiration_date = next(user[1] for user in subscription_data if user[0] == user_id)
        await message.reply_text(
            f"**📅 Your Premium Plan Status**\n\n"
            f"**🆔 User ID**: `{user_id}`\n"
            f"**⏳ Expiration Date**: `{expiration_date}`\n"
            f"**🔒 Status**: *Active*"
        )
    else:
        await message.reply_text("**❌ You are not a premium user.**")

# 4. /add_channel
@bot.on_message(filters.command("add_channel"))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id not in channels:
            channels.append(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} added.")
        else:
            await message.reply_text(f"Channel {channel_id} is already added.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /add_channel <channel_id>")
      
# 5. /remove_channels
@bot.on_message(filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id in channels:
            channels.remove(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} removed.")
        else:
            await message.reply_text(f"Channel {channel_id} is not in the list.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /remove_channels <channel_id>")

# /id Command
@bot.on_message(filters.command("id"))
async def id_command(client, message: Message):
    if message.chat.type == "private":
        # For private chats, return the user ID
        user_id = message.from_user.id
        await message.reply_text(
            f"🎉 **Success!**\n\n"
            f"🆔 **Your User ID:**\n`{user_id}`\n\n"
            f"📌 **Use this ID for further requests.**"
            f"`/adduser {user_id} {expiration_date}`"
        )
    else:
        # For groups or channels, return the chat ID with -100 prefix
        chat_id = message.chat.id
        await message.reply_text(
            f"✅ **Success!**\n\n"
            f"🆔 **This Group/Channel ID:**\n`{chat_id}`\n\n"
            f"📌 **Use this ID for further requests.**\n\n"
            f"To link this group/channel, use the following command:\n"
            f"`/add_channel {chat_id}`"
        )

YOUR_ADMIN_ID = 7696342661

# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == YOUR_ADMIN_ID

# Command to show all allowed channels (Admin only)
@bot.on_message(filters.command("allowed_channels"))
async def allowed_channels(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    channels = read_channels_data()
    if channels:
        channels_list = "\n".join([f"- {channel}" for channel in channels])
        await message.reply_text(f"**📋 Allowed Channels:**\n\n{channels_list}")
    else:
        await message.reply_text("ℹ️ No channels are currently allowed.")

# Command to remove all channels (Admin only)
@bot.on_message(filters.command("remove_all_channels"))
async def remove_all_channels(client, message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Clear the channels data
    write_channels_data([])
    await message.reply_text("✅ **All channels have been removed successfully.**")

# 6. /stop
@bot.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    if message.chat.type == "private":
        user_id = str(message.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await message.reply_text("😔 You are not a premium user. Please subscribe to get access! 🔒")
            return
    else:
        channels = read_channels_data()
        if str(message.chat.id) not in channels:
            await message.reply_text("🚫 You are not a premium user. Subscribe to unlock all features! ✨")
            return

    await message.reply_text("🚦STOPPED🚦" , True)
    os.execl(sys.executable, sys.executable, *sys.argv)
    
cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

@bot.on_message(filters.command("rowdy"))
async def moni_handler(client: Client, m: Message):
    if m.chat.type == "private":
        user_id = str(m.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await m.reply_text("❌ You are not a premium user. Please upgrade your subscription! 💎")
            return
    else:
        channels = read_channels_data()
        if str(m.chat.id) not in channels:
            await m.reply_text("❗ You are not a premium user. Subscribe now for exclusive access! 🚀")
            return
  
    editable = await m.reply_text(f"**Send your txt file 🗃️**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = f"rowdy"
    token = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzYxNTE3MzAuMTI2LCJkYXRhIjp7Il9pZCI6IjYzMDRjMmY3Yzc5NjBlMDAxODAwNDQ4NyIsInVzZXJuYW1lIjoiNzc2MTAxNzc3MCIsImZpcnN0TmFtZSI6IkplZXYgbmFyYXlhbiIsImxhc3ROYW1lIjoic2FoIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sImVtYWlsIjoiV1dXLkpFRVZOQVJBWUFOU0FIQEdNQUlMLkNPTSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTczNTU0NjkzMH0.iImf90mFu_cI-xINBv4t0jVz-rWK1zeXOIwIFvkrS0M"
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("**Enter Batch Name otherwise send `d` grabbing batch name from your file**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Choose your resolution 🎥\n144\n240\n360\n480\n720\n1080\n\n")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter A Caption To Add Otherwise Send `no`\n**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    # Default credit message
    credit = "️ᏒᎾᏯᎠᎽ"
    if raw_text3 == '1':
        CR = 'ᏒᎾᏯᎠᎽ'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
        
    await editable.edit("**Enter Your PW Token For MPD URL  or send no for use default**")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)
    if raw_text4 == 'no':
        MR = token
    else:
        MR = raw_text4
        
    await editable.edit("Now send the **Thumb url**\n**Eg :** ``\n\nor Send `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    count =int(raw_text)    
    try:
        for i in range(arg-1, len(links)):

            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url or "alisg-cdn-a.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
             
            elif '/master.mpd' in url:
             vid_id =  url.split("/")[-2]
             url =  f"https://madxapi-d0cbf6ac738c.herokuapp.com/{vid_id}/master.m3u8?token={raw_text4}"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'
            
            if 'cpvod.testbook.com' in url:
               url = requests.get(f'https://mon-key-3612a8154345.herokuapp.com/get_keys?url=https://cpvod.testbook.com/65f02cbd734b790a42d7317f/playlist.m3u8', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
                   
            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront.net/")
                    print(url)
                else: 
                    url = url    

                print("mpd check")
                key = await helper.get_drm_keys(url)
                print(key)
                await m.reply_text(f"got keys form api : \n`{key}`")
          
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")

            

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**╭━━━━━━━━━━━╮\n🎥 VIDEO ID: {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯**\n\n📄 **Title** : {name1} {res} .mkv\n\n🔖 **Batch Name** : {b_name}**\n\n📥 Extracted By** : {CR}'
                cc1 = f'**╭━━━━━━━━━━━╮\n📁 FILE ID: {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯**\n\n📄 **Title** : {name1} .pdf\n\n🔖 **Batch Name** : {b_name}**\n\n📥 Extracted By** : {CR}'                           
                cczip = f'**╭━━━━━━━━━━━╮\n🎥 VIDEO ID: {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯**\n\n📄 **Title** : {name1} {res} .mkv\n\n🔖 **Batch Name** : {b_name}**\n\n📥 Extracted By** : {CR}'
                cczip= f'**╭━━━━━━━━━━━╮\n📁 FILE ID: {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯**\n\n📄 **Title** : {name1} .pdf\n\n🔖 **Batch Name** : {b_name}**\n\n📥 Extracted By** : {CR}'                           
                  
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue 

                 
                else:
                    Show = f"**📩 𝐃𝐨𝐰𝐥𝐨𝐚𝐝𝐢𝐧𝐠 📩...**\n\n 📝 𝐓𝐢𝐭𝐥𝐞 : `{name}\n\n 🎥 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 :  {raw_text2}`\n\n 🔗 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐥𝐢𝐧𝐤 : {str(count).zfill(3)}\n\n 🖇️ 𝐓𝐨𝐭𝐚𝐥 𝐥𝐢𝐧𝐤𝐬 : {len(links)}\n\n 🔗 𝐔𝐑𝐋 : `{url}`\n\n**╰──────⌈🌟 ᏒᎾᏯᎠᎽ 🌟⌋──────╯**"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)
           
            except Exception as e:
                await m.reply_text(
                    f"** 📥 Downloading... interrupted  **\n\n 𝐍𝐚𝐦𝐞 : {name}\n\n 𝐋𝐢𝐧𝐤 : `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("DONE BOSS 🦁")



bot.run()
if __name__ == "__main__":
    asyncio.run(main())
