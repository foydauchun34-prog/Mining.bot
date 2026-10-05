import telebot
from telebot import types

from config import BOT_TOKEN
from database import init_db, add_user


bot = telebot.TeleBot(BOT_TOKEN)

init_db()


def main_menu():

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    keyboard.row(
        "⛏ Mining",
        "💰 Balans"
    )

    keyboard.row(
        "🎁 Kunlik bonus",
        "👥 Referal"
    )

    keyboard.row(
        "📋 Vazifalar",
        "💎 TON Wallet"
    )

    keyboard.row(
        "🚀 Boost",
        "👑 VIP"
    )

    keyboard.row(
        "🛒 Do‘kon",
        "🧮 Kalkulyator"
    )

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
        "👋 Assalomu alaykum!\n\n"
        "⛏ TON Mining botiga xush kelibsiz.\n\n"
        "Kerakli bo‘limni tanlang:"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda message: True)
def other_messages(message):

    bot.send_message(
        message.chat.id,
        "⬇️ Menyudan bo‘limni tanlang.",
        reply_markup=main_menu()
    )


print("🤖 Bot ishga tushdi...")

bot.infinity_polling()
