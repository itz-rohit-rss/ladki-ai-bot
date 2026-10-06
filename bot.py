import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8906457060:AAEKjnkzaMvnoIj8KubjPtKBYtAs1B80uKQ"

# Render ke liye dummy web server taaki Port scan pass ho jaye
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name if update.effective_user else "Dost"
    await update.message.reply_text(
        f"Hii {name}! ✨ Main Kitty hu.\n"
        "Commands:\n"
        "/joke - Mazedaar joke ke liye\n"
        "/quiz - Sawal khelne ke liye"
    )

# /joke command
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Teacher: Kal school kyu nahi aaye? Pappu: Mam kal sapne me abroad chala gaya tha! 😂",
        "Maine socha dieting shuru karu, phir yaad aaya kismat me khana likha hai! 😜",
        "Zindagi me do hi cheezein mushkil hain: subah jaldi uthna aur time par sona! 😴"
    ]
    await update.message.reply_text(random.choice(jokes))

# /quiz command
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quizzes = [
        "Sawal: Aisi kaunsi cheez hai jo subah 4 taang par, dopahar ko 2 taang par aur shaam ko 3 taang par chalti hai? 🤔\n(Jawab: Insaan)",
        "Sawal: Aisi kaunsi jagah hai jahan 100 log jaate hain toh 101 log wapas aate hain? 😉\n(Jawab: Baarat)",
        "Sawal: Wo kya hai jise aap jitna aage badhate ho, wo utni hi peeche chhoot jaati hai? 👣\n(Jawab: Kadam)"
    ]
    await update.message.reply_text(random.choice(quizzes))

# Group chat & Smart Reply Handler
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    # Koi bhi bot message bheje toh ignore
    if update.effective_user.is_bot:
        return

    sender_name = update.effective_user.first_name or "Dost"
    
    # Text safe handle (photo/sticker hone par crash na ho)
    raw_text = update.message.text or update.message.caption or ""
    msg_text = raw_text.lower()
    bot_id = context.bot.id

    # 1. Jab kisi ne BOT ke message par reply kiya ho
    if update.message.reply_to_message and update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.id == bot_id:
        if any(w in msg_text for w in ["shut up", "chup", "shutup", "bhag"]):
            responses = [
                f"Arey gussa kyu ho rahe ho {sender_name}? Theek hai main chup ho jati hu 🥺",
                f"Haww {sender_name}! Itna gussa accha nahi hota 🙈",
                f"Sorry na {sender_name}! Ab tang nahi karungi pakka 🤐"
            ]
        elif any(w in msg_text for w in ["bolo", "kya", "sunao", "ha bolo"]):
            responses = [
                f"Bas main toh yahi keh rahi thi ki group me masti chal rahi hai! 😄",
                f"Hehe kuch nahi {sender_name}, bas sabki baatein padh rahi thi ✨",
                f"Bolo {sender_name}, main hamesha sunne ke liye taiyaar hu! 😉"
            ]
        elif any(w in msg_text for w in ["sorry", "maaf"]):
            responses = [
                f"Koi baat nahi {sender_name}, maine maaf kiya! ❤️",
                f"It's okay dost, itni pyari dosti me sorry nahi bolte! ✨"
            ]
        else:
            responses = [
                f"Mujhse keh rahe ho kya {sender_name}? Main toh bas aap sabse dosti kar rahi thi ✨",
                f"Hehe {sender_name}, aapki har baat sweet lagti hai! 🌸",
                f"Acha ji {sender_name}? Sach me? 😄"
            ]
        await update.message.reply_text(random.choice(responses))
        return

    # 2. Jab do REAL members aapas me swipe/reply karein
    if update.message.reply_to_message:
        replied_user = update.message.reply_to_message.from_user
        if replied_user and not replied_user.is_bot and replied_user.id != update.effective_user.id:
            replied_name = replied_user.first_name or "Dost"
            if random.random() < 0.35:
                replies_swipe = [
                    f"Arey {replied_name}, suno na! {sender_name} aapse kuch keh rahe hain 😉",
                    f"Dekho {replied_name}, {sender_name} ne aapko reply kiya hai ✨",
                    f"Oho {replied_name}! {sender_name} ki baat suno pehle! 😜"
                ]
                await update.message.reply_text(random.choice(replies_swipe))
            return

    # 3. Direct bulane par
    bot_names = ["kitty", "priya"]
    if any(name in msg_text for name in bot_names):
        if any(w in msg_text for w in ["kaisi ho", "kya haal", "kaise ho"]):
            await update.message.reply_text(f"Main bilkul theek hu {sender_name}! Aap batao? ✨")
        else:
            replies = [
                f"Haan ji {sender_name}, bolo main sun rahi hu! 😊",
                f"Arey {sender_name}, mujhe bulaya kya? ✨",
                f"Bolo {sender_name}, main yahin hu!"
            ]
            await update.message.reply_text(random.choice(replies))

def main():
    # Flask web server background thread me start karein (Render port check ke liye)
    threading.Thread(target=run_web, daemon=True).start()

    # Telegram bot start karein
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), chat_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
    
