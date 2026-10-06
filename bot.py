import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8906457060:AAEKjnkzaMvnoIj8KubjPtKBYtAs1B80uKQ"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hii {name}! ✨ Main Priya hu.\n"
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

    # Agar message bhejne wala koi bot hai, toh ignore karein
    if update.effective_user.is_bot:
        return

    sender_name = update.effective_user.first_name
    msg_text = update.message.text.lower() if update.message.text else ""

    # Agar kisi ne message par swipe / reply kiya hai
    if update.message.reply_to_message:
        replied_user = update.message.reply_to_message.from_user
        
        # Agar reply kisi bot ko kiya gaya hai, toh bot chup rahega (loop spam nahi hoga)
        if replied_user and not replied_user.is_bot:
            replied_name = replied_user.first_name
            # Khud ke message par khud reply na kare
            if replied_user.id != update.effective_user.id:
                replies_swipe = [
                    f"Arey {replied_name}, suno na! {sender_name} aapse kuch keh rahe hain 😉",
                    f"Dekho {replied_name}, {sender_name} ne aapke message par reply kiya hai ✨",
                    f"Oho {replied_name}! {sender_name} ki baat suno pehle! 😜"
                ]
                await update.message.reply_text(random.choice(replies_swipe))
                return

    # Normal Chat Trigger (Jab specifically Priya ya bot se baat karein)
    bot_names = ["priya", "kitty", "bot"]
    is_calling_bot = any(name in msg_text for name in bot_names)

    if any(w in msg_text for w in ["kaisi ho", "kya haal", "kaise ho"]):
        await update.message.reply_text(f"Main bilkul mast hu {sender_name}! Aap batao aapka din kaisa raha? ✨")
    elif any(w in msg_text for w in ["kya kar rahi ho", "kya chal raha"]):
        await update.message.reply_text(f"Bas group me sabki baatein sun rahi hu {sender_name}! Aap sunao?")
    elif any(w in msg_text for w in ["bye", "alvida", "gn", "good night"]):
        await update.message.reply_text(f"Itni jaldi ja rahe ho {sender_name}? Theek hai, take care! ❤️")
    elif is_calling_bot:
        random_replies = [
            f"Haan ji {sender_name}, bolo main sun rahi hu! 😊",
            f"Arey {sender_name}, mujhe bulaya kya? ✨",
            f"Bolo {sender_name}, main yahin hu!"
        ]
        await update.message.reply_text(random.choice(random_replies))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
    
