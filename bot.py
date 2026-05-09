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

# USER DATA
user_balances = {}

# ADMIN IDS
ADMINS = [8721950488]  # replace with your Telegram ID

# USERS TRACKING
total_users = set()


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    total_users.add(user_id)

    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    balance = user_balances[user_id]

    keyboard = [
        [InlineKeyboardButton("🍀 Weed", callback_data="voip")],
        [InlineKeyboardButton("💎 Drugs", callback_data="email")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://i.ibb.co/60SYgbj5/strawberry-with-face-that-says-happy-strawberry-986058-14576.avif",
        caption=f"""
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
# ADMIN PANEL
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("❌ Access denied.")
        return

    total_balance = sum(user_balances.values())

    text = f"""
📊 ADMIN PANEL

👥 Total Users: {len(total_users)}
💰 Total Balance: ₾{total_balance:.2f}

📋 USERS:
"""

    for uid, bal in user_balances.items():
        text += f"\n• {uid} -> ₾{bal:.2f}"

    await update.message.reply_text(text)


# =========================
# CALLBACK HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    balance = user_balances.get(user_id, 0.00)

    if query.data == "voip":

        keyboard = [
            [InlineKeyboardButton("Afghan Kush 0.5G - Sanzona", callback_data="usa_numbers")],
            [InlineKeyboardButton("Afghan Kush 1G - Sanzona", callback_data="canada_numbers")],
            [InlineKeyboardButton("Afghan Kush 3G - Temka", callback_data="federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"🍀 Weed\n\n💰 Balance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "email":

        keyboard = [
            [InlineKeyboardButton("Colombian Cocaine 1G - Temka", callback_data="sending")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"💎 Drugs\n\n💰 Balance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "federal":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"Afghan Kush 3G\nPrice: 250₾\nBalance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "usa_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_usa")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"Afghan Kush 0.5G\nPrice: 90₾\nBalance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "canada_numbers":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_canada")],
            [InlineKeyboardButton("⬅ Back", callback_data="voip")]
        ]

        await query.edit_message_text(
            f"Afghan Kush 1G\nPrice: 140₾\nBalance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "sending":

        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_email")],
            [InlineKeyboardButton("⬅ Back", callback_data="email")]
        ]

        await query.edit_message_text(
            f"Item 1G\nPrice: 350₾\nBalance: ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data in ["buy_federal", "buy_usa", "buy_canada", "buy_email"]:

        await query.message.reply_text(
            "❌ Insufficient balance. Please deposit funds.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
            ])
        )

    elif query.data == "deposit":

        await query.edit_message_text(
            f"""
💰 Deposit

Balance: ₾{balance:.2f}

Send LTC to:
LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅ Back", callback_data="back")]
            ])
        )

    elif query.data == "back":

        keyboard = [
            [InlineKeyboardButton("🍀 Weed", callback_data="voip")],
            [InlineKeyboardButton("💎 Drugs", callback_data="email")],
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
        ]

        await query.edit_message_text(
            f"""
Welcome back

User ID: {user_id}
Balance: ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# RUN BOT
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
