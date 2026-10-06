import telebot
from telebot import types

from config import BOT_TOKEN
from database import init_db, add_user

bot = telebot.TeleBot(BOT_TOKEN)

# Your Web App URL
WEB_APP_URL = "https://foydauchun34-prog.github.io/Bot.minee/"

init_db()


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

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

    # Inline button that opens the Web App
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🚀 OPEN MINING APP",
            web_app=types.WebAppInfo(url=WEB_APP_URL)
        )
    )

    text = (
        "👋 Assalomu alaykum!\n\n"
        "⛏ TON Mining botiga xush kelibsiz.\n\n"
        "Web App'ni ochish uchun pastdagi tugmani bosing yoki menyudan bo‘limni tanlang:"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

    # Also send the classic reply keyboard
    bot.send_message(
        message.chat.id,
        "⬇️ Menyudan kerakli bo‘limni tanlang:",
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
