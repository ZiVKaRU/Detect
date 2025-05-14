# bot.py
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import threading

TOKEN = "7668078234:AAGb2v6V-7yGXTPciL3Jlgx869d2JiTMLWc"
AUTHORIZED_USER_ID = 5231100075  # Заменить на ваш ID
WEB_APP_URL = "http://localhost:5000"  # или ngrok URL для внешнего доступа

bot_app = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Открыть приложение", web_app={"url": WEB_APP_URL})
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def send_face_detected(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=AUTHORIZED_USER_ID, text="⚠️ Обнаружен человек!")

def run_bot():
    global bot_app
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    bot_app.run_polling()

if __name__ == "__main__":
    from web import app as flask_app
    from camera import set_bot_app

    set_bot_app(bot_app)

    flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    flask_thread.start()

    run_bot()