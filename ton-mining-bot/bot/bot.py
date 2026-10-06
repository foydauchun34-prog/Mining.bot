import telebot
from telebot import types

from config import BOT_TOKEN
from database import (
    init_db,
    add_user,
    get_user,
    start_mining,
    get_mining_status
)

bot = telebot.TeleBot(BOT_TOKEN)

init_db()

WEB_APP_URL = "https://foydauchun34-prog.github.io/Bot.minee/"


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

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "🚀 OPEN MINING APP",
            web_app=types.WebAppInfo(
                url=WEB_APP_URL
            )
        )
    )

    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum!\n\n"
        "⛏ TON Mining botiga xush kelibsiz!\n\n"
        "Web App'ni ochish uchun tugmani bosing.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "⛏ Mining")
def mining(message):

    user_id = message.from_user.id

    status = get_mining_status(user_id)

    if isinstance(status, dict):
        bot.send_message(
            message.chat.id,
            "⛏ Mining allaqachon ishlayapti.\n\n"
            f"⏰ Tugash vaqti:\n{status['ends_at']}"
        )
        return

    if status == "finished":
        bot.send_message(
            message.chat.id,
            "⏰ Oldingi mining sessiyasi tugagan.\n"
            "Yangi sessiyani boshlashingiz mumkin."
        )

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "▶️ START MINING",
            callback_data="start_mining"
        )
    )

    bot.send_message(
        message.chat.id,
        "⛏ Mining\n\n"
        "24 soatlik mining sessiyasini boshlash uchun "
        "quyidagi tugmani bosing.",
        reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "start_mining"
)
def start_mining_callback(call):

    user_id = call.from_user.id

    success, result = start_mining(user_id)

    if not success:
        bot.answer_callback_query(
            call.id,
            result,
            show_alert=True
        )
        return

    bot.answer_callback_query(
        call.id,
        "Mining boshlandi!"
    )

    bot.edit_message_text(
        "🟢 Mining boshlandi!\n\n"
        "⏱ Davomiyligi: 24 soat\n"
        f"⏰ Tugash vaqti: {result.strftime('%Y-%m-%d %H:%M:%S')}",
        call.message.chat.id,
        call.message.message_id
    )


@bot.message_handler(func=lambda message: message.text == "💰 Balans")
def balance(message):

    user = get_user(message.from_user.id)

    if not user:
        add_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )
        user = get_user(message.from_user.id)

    balance_value = user[3]

    bot.send_message(
        message.chat.id,
        f"💰 Sizning balansingiz:\n\n"
        f"💎 {balance_value:.4f} TON"
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
