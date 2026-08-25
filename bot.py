import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BAD_WORDS = ["anjing", "babi", "bangsat", "tolol"]
GROUP_LINK = "https://t.me/fFHRIYYCAJg3YmVl"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 Security Bot Aktif!")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
            
        user_name = member.first_name
        share_url = f"https://t.me/share/url?url={GROUP_LINK}&text=Gabung%20yuk%20ke%20grup%20ini!"
        
        keyboard = [
            [InlineKeyboardButton("📤 Bagikan Link Grup Ini", url=share_url)],
            [InlineKeyboardButton("🔗 Kunjungi Grup", url=GROUP_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        pesan = (
            f"👋 Halo {user_name}, Selamat datang di grup! 🎉\n\n"
            f"⚠️ **PERATURAN / SYARAT UTAMA:**\n"
            f"Sebelum bergabung lebih jauh, kamu **wajib membagikan (share)** link grup ini terlebih dahulu ke teman atau chat lain menggunakan tombol di bawah ya! 👇"
        )
        
        await update.message.reply_text(pesan, reply_markup=reply_markup)

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 ATURAN:\n1. Wajib share link grup saat bergabung.\n2. Dilarang kata kasar/toxic.")

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔗 **Tautan Resmi Grup:**\n{GROUP_LINK}")

async def filter_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    for word in BAD_WORDS:
        if word in text:
            user = update.message.from_user.first_name
            await update.message.reply_text(f"⚠️ Peringatan untuk {user}! Jangan menggunakan kata kasar.")
            break

def main():
    TOKEN = "8959556595:AAG4_eo3Wix0LVHSgzoGpfKdyV_2u9uUbMs"
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("link", link_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_chat))
    
    print("Security Bot dengan Link Grup Publik berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
