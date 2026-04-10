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
    urls = ["https://www.reuters.com/business/", "https://www.cnbc.com/world/?region=world"]
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in urls:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            if "reuters" in url:
                titles = soup.find_all(['h2', 'h3'], limit=5)
            else:
                titles = soup.find_all('a', class_='Card-title', limit=5)
            for t in titles:
                text = t.get_text().strip()
                if len(text) > 25: news_list.append(text)
    except: pass
    return list(set(news_list))[:5]

async def send_report(context: ContextTypes.DEFAULT_TYPE):
    news = get_finance_news()
    if not news: return
    
    header = f"📅 **{datetime.datetime.now().strftime('%d/%m/%Y')} FİNANS RAPORU**\n\n"
    tweets = ""
    for i, item in enumerate(news, 1):
        tweet_text = f"🔹 {item}\n\nAnaliz: Küresel piyasalarda bu gelişme volatiliteyi artırabilir. Kritik seviyeler takip edilmeli.\n\n#Finans #Ekonomi #Borsa"
        tweets += f"📝 **Tweet Taslağı {i}:**\n`{tweet_text[:340]}`\n\n"
    
    await context.bot.send_message(chat_id=MY_ID, text=header + tweets, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    keyboard = [[InlineKeyboardButton("📊 Şimdi Analiz Et", callback_query_data='analiz_yap')]]
    await update.message.reply_text("Selam! Her sabah 10:00'da raporun gelecek. İstersen butona basıp şimdi de alabilirsin.", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await send_report(context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue

    # Türkiye saatiyle sabah 10:00 ayarı
    tr_time = datetime.time(hour=10, minute=0, second=0, tzinfo=pytz.timezone('Europe/Istanbul'))
    job_queue.run_daily(send_report, time=tr_time)

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot başlatılıyor...")
    application.run_polling()
