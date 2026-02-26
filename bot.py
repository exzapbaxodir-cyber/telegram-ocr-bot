import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pytesseract
from PIL import Image
import os

# Agar Windows bo'lsa, tesseract path yoz:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

TOKEN = "8715156014:AAHCjemXkinxWLOZket-uMjlt4huBXbqQJ8"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! 👋\nMenga rasm yubor, ichidagi matnni o‘qib beraman.")

# Rasm kelganda
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = "image.jpg"
    await file.download_to_drive(file_path)

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

        if text.strip() == "":
            await update.message.reply_text("Rasmda matn topilmadi 😔")
        else:
            await update.message.reply_text(f"📄 Rasm ichidagi matn:\n\n{text}")

    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi ❌")

    if os.path.exists(file_path):
        os.remove(file_path)

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
