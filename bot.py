import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Aapka Bot Token
TOKEN = "8906457060:AAEKjnkzaMvnoIj8KubjPtKBYtAs1B80uKQ"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hii {name}! ✨ Main Priya hu.\n"
        "Mujhse normal chat kar sakte ho ya try karo:\n"
        "/joke - Mazedaar joke sunne ke liye\n"
        "/quiz - Ek chota sawal khelne ke liye"
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
        "Sawal: Aisi kaunsi cheez hai jo subah 4 taang par, dopahar ko 2 taang par aur shaam ko 3 taang par chalti hai? 🤔 (Jawab: Insaan)",
        "Sawal: Aisi kaunsi jagah hai jahan 100 log jaate hain toh 101 log wapas aate hain? 😉 (Jawab: Baarat)",
        "Sawal: Wo kya hai jise aap jitna aage badhate ho, wo utni hi peeche chhoot jaati hai? 👣 (Jawab: Kadam)"
    ]
    await update.message.reply_text(random.choice(quizzes))

# Group chat, Reply/Swipe & AI Ladki style responses
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_name = update.effective_user.first_name
    msg_text = update.message.text.lower() if update.message.text else ""

    # Agar kisi ne message par swipe/reply kiya hai
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        replied_user = update.message.reply_to_message.from_user.first_name
        replies_swipe = [
            f"Arey {replied_user}, suno na! {sender_name} aapse kuch keh rahe hain 😉",
            f"Dekho {replied_user}, {sender_name} ne aapke message par reply kiya hai ✨",
            f"Oho {replied_user}! {sender_name} ki baat suno pehle! 😜"
        ]
        await update.message.reply_text(random.choice(replies_swipe))
        return

    # Normal Chat Responses (Ladki persona)
    if any(w in msg_text for w in ["kaisi ho", "kya haal", "kaise ho"]):
        await update.message.reply_text(f"Main bilkul mast hu {sender_name}! Aap batao aapka din kaisa raha? ✨")
    elif any(w in msg_text for w in ["kya kar rahi ho", "kya chal raha"]):
        await update.message.reply_text(f"Bas group me baatein sun rahi hu {sender_name}! Aap sunao kya chal raha hai?")
    elif any(w in msg_text for w in ["bye", "alvida", "gn", "good night"]):
        await update.message.reply_text(f"Itni jaldi ja rahe ho {sender_name}? Theek hai, take care & good night! ❤️")
    else:
        random_replies = [
            f"Acha ji {sender_name}? Sach me? 😄",
            f"Haan {sender_name}, bolo main sun rahi hu!",
            f"Hehe {sender_name}, sahi keh rahe ho! Aur sunao kuch mazedaar? ✨",
            f"Suno {sender_name}, bore ho rahe ho kya? /joke likh kar try karo!"
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
  
