import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os

TOKEN= os.environ.get("TOKEN")

if not TOKEN:
    raise Exception("TOKEN is NOT loaded from Railway Variables")

PRIVATE_LINK = "https://t.me/+e4D7AQ8qlhk5MGY5"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("⭐ Купить за 100 Stars", callback_data="stars")],
        [InlineKeyboardButton("💳 Банковская карта", callback_data="card")]
    ]

    await update.message.reply_text(
        "👋 Всем привет!\n\n"
        "Если хочешь купить мою приватку — выбери способ оплаты 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "stars":

        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="Приватка",
            description="Доступ к приватке",
            payload="privat_stars_100",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Доступ", 100)]
        )

    elif query.data == "card":
        await query.edit_message_text("💳 Оплата картой\n\n⏳ Скоро будет доступно")


# обязательный precheckout
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# успешная оплата
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Оплата прошла успешно!\n\n"
        f"Вот твоя ссылка:\n{PRIVATE_LINK}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
app.add_handler(MessageHandler(filters.PRE_CHECKOUT_QUERY, precheckout))

app.run_polling()
