import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from pytube import YouTube
from dotenv import load_dotenv

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# .env faylini yuklash
load_dotenv()

# Tokenni olish
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start buyrug'i uchun handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Salom! Men YouTube-dan media yuklab oluvchi botman. YouTube video linkini yuboring.')

# Video yuklash uchun handler
def download_video(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    url = update.message.text

    try:
        # Yuklab olish papkasini belgilash
        download_folder = 'downloads'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = video.download(output_path=download_folder)

        # Faylni yuborish
        with open(video_path, 'rb') as video_file:
            context.bot.send_video(chat_id=chat_id, video=video_file)

        # Faylni o'chirish
        os.remove(video_path)
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        update.message.reply_text('Video yuklab olishda xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.')

def main() -> None:
    # Updater va Dispatcher yaratish
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handlerni qo'shish
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Botni ishga tushurish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
