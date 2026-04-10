import logging
import requests
import datetime
import pytz
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Ayarlar
TOKEN = "8267555325:AAE_HZbu1YNNFB3_DSXUSrq2NqiAvFJbO90"
MY_ID = 577929906

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_finance_news():
    news_list = []
    # Reuters ve CNBC bazen botları engeller, o yüzden User-Agent çok önemli
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        # CNBC denemesi
        r = requests.get("https://www.cnbc.com/world/?region=world", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        titles = soup.find_all('a', class_='Card-title', limit=5)
        for t in titles:
            news_list.append(t.get_text().strip())
    except Exception as e:
        logging.error(f"Haber çekme hatası: {e}")

    # Eğer haber çekilemezse boş kalmasın diye yedek
    if not news_list:
        news_list = ["Piyasalarda genel görünüm takip ediliyor.", "Küresel ekonomik veriler bekleniyor."]
        
    return list(set(news_list))[:5]

async def send_report(context: ContextTypes.DEFAULT_TYPE):
    news = get_finance_news()
    header = f"📅 **{datetime.datetime.now().strftime('%d/%m/%Y')} FİNANS RAPORU**\n\n"
    tweets = ""
    for i, item in enumerate(news, 1):
        tweet_text = f"🔹 {item}\n\nAnaliz: Küresel piyasalarda bu gelişme volatiliteyi artırabilir. Kritik seviyeler takip edilmeli.\n\n#Finans #Ekonomi #Borsa"
        tweets += f"📝 **Tweet Taslağı {i}:**\n`{tweet_text[:340]}`\n\n"
    
    await context.bot.send_message(chat_id=MY_ID, text=header + tweets, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    keyboard = [[InlineKeyboardButton("📊 Şimdi Analiz Et", callback_query_data='analiz_yap')]]
    await update.message.reply_text("Sistem Aktif! \n\nHer sabah 10:00'da raporun gelecek.\nİstersen butona basıp şimdi test edebilirsin.", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("🔄 Analiz hazırlanıyor, lütfen bekleyin...")
    await send_report(context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Zamanlayıcıyı kur (Bot başlar başlamaz kontrol eder)
    if application.job_queue:
        tr_tz = pytz.timezone('Europe/Istanbul')
        tr_time = datetime.time(hour=10, minute=0, second=0, tzinfo=tr_tz)
        application.job_queue.run_daily(send_report, time=tr_time)
        logging.info("Zamanlayıcı 10:00 için kuruldu.")

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()
