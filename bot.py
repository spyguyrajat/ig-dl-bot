import os
import subprocess
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /get <instagram_username> to download profile.")

async def get_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a username. Usage: /get username")
        return

    username = context.args[0]
    await update.message.reply_text(f"Downloading profile for @{username}...")

    try:
        subprocess.run(['instagram_profile_downloader', username], check=True)

        folder_path = os.path.join(os.getcwd(), username)
        zip_path = f"{folder_path}.zip"

        if os.path.exists(folder_path):
            shutil.make_archive(folder_path, 'zip', folder_path)
            await update.message.reply_document(document=open(zip_path, 'rb'))

            shutil.rmtree(folder_path)
            os.remove(zip_path)
        else:
            await update.message.reply_text("No files found. Something went wrong.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_profile))
    app.run_polling()

if __name__ == '__main__':
    main()
