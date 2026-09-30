import telebot
from telebot import types

from config import BOT_TOKEN
from database import init_db, add_user, get_user


bot = telebot.TeleBot(BOT_TOKEN)

init_db()


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    keyboard.row("⛏ Mining", "💰 Balans")
    keyboard.row("🎁 Kunlik bonus", "👥 Referal")
    keyboard.row("📋 Vazifalar", "💎 TON Wallet")
    keyboard.row("🚀 Boost", "👑 VIP")
    keyboard.row("🛒 Do‘kon", "🧮 Kalkulyator")

    return keyboard


@bot.message_handler(commands=["start"])
def start(message):

    user = message.from_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    text = (
        f"👋 Salom, {user.first_name}!\n\n"
        "🤖 TON Mining botiga xush kelibsiz.\n\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang:"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda message: message.text == "💰 Balans")
def balance(message):

    user = get_user(message.from_user.id)

    balance_value = user[3] if user else 0

    bot.send_message(
        message.chat.id,
        f"💰 Balansingiz: {balance_value:.4f} TON"
    )


@bot.message_handler(func=lambda message: message.text == "⛏ Mining")
def mining(message):

    bot.send_message(
        message.chat.id,
        "⛏ Mining bo‘limi\n\n"
        "Bu yerda 24 soatlik mining tizimi ishlaydi.\n\n"
        "🚧 Keyingi bosqichda qo‘shamiz."
    )


print("🤖 Bot ishga tushdi...")

bot.infinity_polling()
