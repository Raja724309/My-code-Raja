
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient
from rembg import remove
from PIL import Image
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

# Configuration (Ab ye Render ke Environment Variables se link uthayega)
TOKEN = os.environ.get("8562390719:AAGo9y6MkqSpHMVxW_9aTabPmEjr8FijFwk")
MONGO_URI = os.environ.get("mongodb+srv://rajapundhir963450_db_user:<mEVu3SVVknbe3WLd>@cluster0.r8n3ro0.mongodb.net/?appName=Cluster0")
SERP_API_KEY = os.environ.get("716c569560f9229b7321d80c14c102b54272efe979c5ee93d6cea9f1d0802443")

# Database
client = MongoClient(MONGO_URI)
db = client.bot_database 
logs_col = db.logs 

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot active hai!\n/trends - AI News\nPhoto bhejo - Background hatane ke liye.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    input_file = f"input_{user_id}.jpg"
    output_file = f"output_{user_id}.png"
    
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive(input_file)
    
    input_img = Image.open(input_file)
    output_img = remove(input_img)
    output_img.save(output_file)
    
    await update.message.reply_photo(photo=open(output_file, "rb"))
    
    if os.path.exists(input_file): os.remove(input_file)
    if os.path.exists(output_file): os.remove(output_file)

async def get_trends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        search = GoogleSearch({"engine": "google", "q": "latest AI news", "api_key": SERP_API_KEY})
        results = search.get_dict().get("organic_results", [])[:3]
        response = "🚀 **Latest Trends:**\n\n" + "\n\n".join([f"• {r['title']}\n🔗 {r['link']}" for r in results])
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Trend load karne mein error aaya.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in ["gaali", "faltu"]):
        logs_col.insert_one({"user_id": update.effective_user.id, "action": "Bad Action"})
        await update.message.reply_text("🚫 Faltu harkat record ho gayi hai.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trends", get_trends))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
