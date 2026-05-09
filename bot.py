from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

# DATA
user_balances = {}
total_users = set()

ADMINS = [123456789]  # replace with your Telegram ID


# =========================
# START (WITH IMAGE)
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    total_users.add(user_id)

    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    balance = user_balances[user_id]

    keyboard = [
        [InlineKeyboardButton("🍀 Digital Pack", callback_data="voip")],
        [InlineKeyboardButton("💎 Premium Access", callback_data="email")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
    ]

    await update.message.reply_photo(
        photo="https://i.ibb.co/60SYgbj5/strawberry-with-face-that-says-happy-strawberry-986058-14576.avif",
        caption=f"""
🍓 Welcome 🍓

👤 User ID: {user_id}
💰 Balance: ₾{balance:.2f}
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# ADMIN PANEL
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("❌ Access denied")
        return

    total_balance = sum(user_balances.values())

    text = f"""
📊 ADMIN PANEL

👥 Users: {len(total_users)}
💰 Total Balance: ₾{total_balance:.2f}

Users:
"""

    for uid, bal in user_balances.items():
        text += f"\n• {uid} -> ₾{bal:.2f}"

    await update.message.reply_text(text)


# =========================
# CALLBACKS
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    balance = user_balances.get(user_id, 0.0)

    # PRODUCT MENU 1
    if query.data == "voip":
        keyboard = [
            [InlineKeyboardButton("Basic Digital Pack - $10", callback_data="item1")],
            [InlineKeyboardButton("Pro Digital Pack - $25", callback_data="item2")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"🍀 Digital Packs\n💰 {balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # PRODUCT MENU 2
    elif query.data == "email":
        keyboard = [
            [InlineKeyboardButton("Premium Access 1 Month - $30", callback_data="item3")],
            [InlineKeyboardButton("⬅ Back", callback_data="back")]
        ]

        await query.edit_message_text(
            f"💎 Premium Menu\n💰 {balance:.2f}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # DEPOSIT
    elif query.data == "deposit":
        await query.edit_message_text(
            f"""
💰 Deposit

Send funds to:
YOUR_WALLET_ADDRESS_HERE

Balance: ₾{balance:.2f}
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅ Back", callback_data="back")]
            ])
        )

    # ITEMS (NO PURCHASE LOGIC YET)
    elif query.data in ["item1", "item2", "item3"]:
        await query.message.reply_text(
            "❌ Payment system not active yet.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
            ])
        )

    # BACK
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("🍀 Digital Pack", callback_data="voip")],
            [InlineKeyboardButton("💎 Premium Access", callback_data="email")],
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
# MAIN (RAILWAY SAFE)
# =========================
if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    # SAFE webhook cleanup
    app.bot.delete_webhook(drop_pending_updates=True)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot Running...")
    app.run_polling()
