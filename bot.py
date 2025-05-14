# bot.py
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "7668078234:AAGb2v6V-7yGXTPciL3Jlgx869d2JiTMLWc"
AUTHORIZED_USER_ID = 5231100075  # Твой Telegram ID
WEB_APP_URL = "https://ваше-приложение.onrender.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Открыть приложение", web_app={"url": WEB_APP_URL})
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def send_face_detected(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=AUTHORIZED_USER_ID, text="⚠️ Обнаружен человек!")

if __name__ == "__main__":
    from web import app as flask_app
    import threading

    flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    flask_thread.start()

    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    bot_app.run_polling()