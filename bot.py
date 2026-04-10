import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8267555325:AAE_HZbu1YNNFB3_DSXUSrq2NqiAvFJbO90"
MY_ID = 577929906

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == MY_ID:
        await update.message.reply_text("Selam cmle#79! Botun Render üzerinden 7/24 çalışıyor. Finans haberlerini bekliyorum.")
    else:
        await update.message.reply_text("Bu bot kişiye özeldir.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == MY_ID:
        await update.message.reply_text(f"Haber kaydedildi: {update.message.text[:30]}...")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
