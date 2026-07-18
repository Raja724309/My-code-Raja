
import os
import asyncio
from pyrogram import Client, filters
from database import init_db, log_bad_action

# Environment variables se keys uthaayein
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("AI_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize database
init_db()

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🤖 **AI Bot Online!**\n\nSend a photo to start processing.")

@app.on_message(filters.text)
async def handle_text(client, message):
    # Security: Bad word filter
    bad_words = ["gali1", "gali2"] # Yahan apni list add karein
    if any(word in message.text.lower() for word in bad_words):
        await message.delete()
        log_bad_action(message.from_user.id, "Used abusive language")
        await client.send_message(message.chat.id, "⚠️ **Warning:** Faltu harkat na karein!")
    else:
        await message.reply("AI mode active hai... Photo bhejiye.")

print("Bot is starting...")
app.run()
