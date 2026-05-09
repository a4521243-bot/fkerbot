import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8721950488
ADMIN_CONTACT = "@mailnovacore"

DEPOSIT_ADDRESS = "LRvMZHB6rYK2cbQWqJf2WhVgNbkUuceBDM"

IMAGE_URL = "https://i.ibb.co/7d0qYBfN/Chat-GPT-Image-May-8-2026-02-51-14-PM.png"

users = set()

# =========================
# PRODUCT INFO
# =========================
PRODUCTS = {
    "virtual": "🍀 Afghan Kush 0.5G\n\n✔ Addresses\n✔ Available\n✔ Sanzona\n💵 Price: ₾85",
    "federal": "🍀 Afghan Kush 1G\n\n✔ Addresses\n✔ Available\n✔ Sanzona\n💵 Price: ₾140",
    "sms": "💎 Coca VHQ 1G\n\n✔ Addresses\n✔ Available\n✔ Temka\n💵 Price: ₾500",
    "email": "💎 Coca VHQ 0.5G\n\n✔ Addresses\n✔ Available\n✔ Gldani\n💵 Price: ₾270",
}

# =========================
# MENU TEXT (SAME FOR START & MENU)
# =========================
def main_menu_caption():
    return (
        "👋 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 MARWKVIBOT\n\n"
        "🔐 Anonymous & Secure Platform\n"
        "⚡ Instant and Very High Quality\n"
        "💎 Payment: Litecoin (LTC)\n\n"
        "📍Locations: Tbilisi\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👇 Choose a product below:"
    )

# =========================
# MENU BUTTONS
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍀 Afghan Kush 0.5G - 85₾", callback_data="virtual")],
        [InlineKeyboardButton("🍀 Afghan Kush 1G - 140₾", callback_data="federal")],
        [InlineKeyboardButton("💎 Coca VHQ 1G - 500₾", callback_data="sms")],
        [InlineKeyboardButton("💎 Coca VHQ 0.5G - 270₾", callback_data="email")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💳 Deposit LTC", callback_data="deposit")]
    ])

# =========================
# START (IMAGE + WELCOME)
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption=main_menu_caption(),
        reply_markup=main_menu()
    )

# =========================
# ADMIN PANEL
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Stats", callback_data="admin_stats")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
        ])
    )

# =========================
# CALLBACK HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    msg = query.message

    # ================= SERVICES =================
    if query.data in PRODUCTS:
        await msg.reply_text(
            PRODUCTS[query.data],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data=f"buy_{query.data}")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BUY =================
    elif query.data.startswith("buy_"):

        service = query.data.replace("buy_", "")

        await msg.reply_text(
            f"🛒 ORDER CONFIRMATION\n\n"
            f"{PRODUCTS.get(service, '')}\n\n"
            "💎 Payment: Litecoin (LTC)\n\n"
            f"📩 Address:\n`{DEPOSIT_ADDRESS}`\n\n"
            "⚡ Tap & hold to copy\n\n"
            f"👨‍💻 Support: {ADMIN_CONTACT}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy Address", callback_data="copy")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= COPY =================
    elif query.data == "copy":
        await msg.reply_text(
            f"📋 LTC ADDRESS:\n\n`{DEPOSIT_ADDRESS}`\n\n⚡ Tap & hold to copy",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= BALANCE =================
    elif query.data == "balance":
        await msg.reply_text(
            "💰 BALANCE: $0\n💎 SYSTEM: LTC WALLET\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= DEPOSIT =================
    elif query.data == "deposit":
        await msg.reply_text(
            "💳 LTC DEPOSIT\n\n"
            f"📩 Address:\n`{DEPOSIT_ADDRESS}`\n\n"
            "⚡ Tap & hold to copy\n\n"
            f"👨‍💻 {ADMIN_CONTACT}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy Address", callback_data="copy")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= ADMIN STATS =================
    elif query.data == "admin_stats":

        if query.from_user.id != ADMIN_ID:
            return

        await msg.reply_text(
            f"📊 USERS: {len(users)}\n\n💰 SYSTEM ACTIVE",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )

    # ================= MENU =================
    elif query.data == "menu":
        await msg.reply_text(
            main_menu_caption(),
            reply_markup=main_menu()
        )

# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
