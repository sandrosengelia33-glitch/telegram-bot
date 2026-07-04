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

Token = os.getenv("Token")

PRIVATE_LINK = "https://t.me/+e4D7AQ8qlhk5MGY5"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("⭐ Купить за 100 Stars", callback_data="stars")],
        [InlineKeyboardButton("💳 Банковская карта", callback_data="card")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Всем привет!\n\n"
        "Если хочешь купить мою приватку — выбери способ оплаты 👇",
        reply_markup=reply_markup
    )


# кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ⭐ Stars оплата
    if query.data == "stars":

        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="Приватка",
            description="Доступ к приватке",
            payload="privat_stars_100",
            provider_token="",   # важно для Stars
            currency="XTR",
            prices=[LabeledPrice("Доступ", 100)]
        )

    # 💳 заглушка карты
    elif query.data == "card":
        await query.edit_message_text(
            "💳 Оплата картой\n\n⏳ Скоро будет доступно"
        )


# обязательное подтверждение оплаты
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# успешная оплата
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Оплата прошла успешно!\n\n"
        f"Вот твоя ссылка на приват:\n{PRIVATE_LINK}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
app.add_handler(CallbackQueryHandler(precheckout, pattern="pre_checkout_query"))

app.run_polling()
