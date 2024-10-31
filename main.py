import logging
import json
from telegram.error import BadRequest
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7761506489:AAG_GzsRxIdplwWeEK3svvglHUmuvN4vgeg'

ADMIN_CHAT_ID = 1547040457
SUBSCRIBERS_FILE = 'subscribers.json'
CHANNEL_USERNAME = '@mr_makhammatovs'
CHANNEL_INVITE_LINK = 't.me/mr_makhammatovs'
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_subscribers():
    with open(SUBSCRIBERS_FILE, 'w') as file:
        json.dump(subscribers, file)

subscribers = load_subscribers()

async def check_channel_membership(user_id, context: CallbackContext) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except BadRequest as e:
        print(f"Error checking membership: {e}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    is_member = await check_channel_membership(chat_id, context)

    if is_member:
        if chat_id not in subscribers:
            subscribers.append(chat_id)
            save_subscribers()
            await update.message.reply_text("Assalomu alaykum!!!\n"
                                            "Kunlik Hadis botimizga Hush Kelibsiz!!!")
            print(f"Subscribers list updated: {subscribers}")
        else:
            await update.message.reply_text("Siz bu bot foydalanuvchilari ro'yhatida borsiz!!!")
    else:
        await update.message.reply_text(f"Botdan foydalanish uchun avvalo kanalimizga a'zo bo'lishingiz kerak!\n"
                                        f"Kanalingiz: {CHANNEL_INVITE_LINK}")

async def stop(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers()  # Save the updated subscribers list to file
        await update.message.reply_text("Siz botni to'xtattingiz!!!")
    else:
        await update.message.reply_text("Siz bu bot foydalanuvchilari ro'yhatidan topilmadingiz!!!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id == ADMIN_CHAT_ID:
        message_text = update.message.text
        print(f"Subscribers: {subscribers}")
        for subscriber in subscribers:
            try:
                await context.bot.send_message(chat_id=subscriber, text=message_text)
            except Exception as e:
                print(f"Failed to send message to {subscriber}: {e}")
        await update.message.reply_text("HADIS har bir foydalanuvchiga muvaffaqiyatli yuborildi!!!")
    else:
        await update.message.reply_text("Faqatgina Admin bu botga Hadis yubora oladi!!!")

async def handle_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id == ADMIN_CHAT_ID:
        photo = update.message.photo[-1]
        print(f"Subscribers: {subscribers}")
        for subscriber in subscribers:
            try:
                await context.bot.send_photo(chat_id=subscriber, photo=photo.file_id)
            except Exception as e:
                print(f"Failed to send photo to {subscriber}: {e}")
        await update.message.reply_text("Foto har bir foydalanuvchiga muvaffaqiyatli yuborildi!!!")
    else:
        await update.message.reply_text("Faqatgina Admin bu botga Foto yubora oladi!!!")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()

if __name__ == '__main__':
    main()