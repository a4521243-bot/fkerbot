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

# =========================
# DATA
# =========================
user_balances = {}
total_users = set()

ADMINS = [8721950488]  # replace with your Telegram ID


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

    await update.message.reply_photo(
        photo="https://i.ibb.co/60SYgbj5/strawberry-with-face-that-says-happy-strawberry-986058-14576.avif",
        caption=f"""
🍓 Welcome to marwkvibot 🍓
Very High Quality
Addresses✅
Available✅
@marwkvibot

👤 User ID: {user_id}
💰 Balance: ₾{balance:.2f}
📍 Tbilisi
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
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
            [InlineKeyboardButton("Afghan Kush 0.5G", callback_data="usa_numbers")],
            [InlineKeyboardButton("Afghan Kush 1G", callback_data="canada_numbers")],
            [InlineKeyboardButton("Afghan Kush 3G", callback_data="federal")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"🍀 Weed Menu\n💰 ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "email":
        keyboard = [
            [InlineKeyboardButton("Item 1G", callback_data="sending")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"💎 Menu\n💰 ₾{balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "deposit":
        await query.edit_message_text(
            f"""
💰 Deposit

Balance: ₾{balance:.2f}

LTC Address:
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

👤 {user_id}
💰 ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# SAFE RAILWAY START (FIXED)
# =========================
async def post_init(app):
    # 🔥 IMPORTANT FIX FOR RAILWAY + TELEGRAM CONFLICT
    await app.bot.delete_webhook(drop_pending_updates=True)


# =========================
# RUN BOT
# =========================
if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot Running...")
    app.run_polling()
