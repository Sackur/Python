import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Настройка логирования, чтобы видеть ошибки в консоли
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для заданий. Используй /menu, чтобы увидеть команды.")


# Команда /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Доступные команды:\n"
        "/whisper [текст] — сказать шепотом (нижний регистр)\n"
        "/scream [текст] — крикнуть (верхний регистр)"
    )
    await update.message.reply_text(text)


# Команда /whisper
async def whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши что-нибудь после команды /whisper")
        return

    user_text = " ".join(context.args)
    await update.message.reply_text(f" {user_text.lower()}")


# Команда /scream
async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши что-нибудь после команды /scream")
        return

    user_text = " ".join(context.args)
    await update.message.reply_text(f" {user_text.upper()}!!!")


if __name__ == '__main__':
    #Место для токена
    TOKEN = 'токен'

    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('whisper', whisper))
    application.add_handler(CommandHandler('scream', scream))

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    application.run_polling()