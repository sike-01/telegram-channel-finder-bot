import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Use /search <keyword> to find public Telegram channels."
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Please provide a keyword.")
    keyword = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching for: {keyword}")

    url = f"https://tgstat.com/en/search?query={keyword}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".channel-item__title a")

    if not items:
        return await update.message.reply_text("⚠️ No channels found.")
    
    lines = []
    for a in items:
        title = a.text.strip()
        username = a["href"].split("/")[-1]
        lines.append(f"{title}: https://t.me/{username}")
    
    await update.message.reply_text("\n".join(lines))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.run_polling()
