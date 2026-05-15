from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8721950488

users = set()
balances = {}

BTC_WALLET = "1PNRb6zsiyPc3oRjZuPWLqQSKptxkXWhiB"


# PRODUCTS
products = {
    "tier2": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 270,
        "description": "სთეიჯი: Tier#2 - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026",
    },
    "tier1": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 320,
        "description": "სთეიჯი: Tier#1 - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026",
    },
    "tool": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 500,
        "description": "სთეიჯი: Orbit - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026",
    },
    "tlst": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 1500,
        "description": "სთეიჯი: VIP - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026",
    },
}


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 ვიტრინა", callback_data="shop")],
        [InlineKeyboardButton("💰 ბალანსი", callback_data="balance")],
        [InlineKeyboardButton("🎫 ჩემი ბილეთები", callback_data="mytickets")],
        [InlineKeyboardButton("🔐 ადმინი", callback_data="admin")],
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎟️ ბილეთები", callback_data="leads")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    if user_id not in balances:
        balances[user_id] = 0

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 კეთილი იყოს თქვენი მობრძანება!",
        reply_markup=main_menu()
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_id not in balances:
        balances[user_id] = 0

    # BACK
    if data == "back":
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🏠 მთავარი მენიუ",
            reply_markup=main_menu()
        )

    elif data == "shop":
        await query.edit_message_text(
            "🛒 ვიტრინა",
            reply_markup=shop_menu()
        )

    elif data == "balance":
        await query.edit_message_text(
            f"💰 ბალანსი: ₾{balances[user_id]}",
            reply_markup=main_menu()
        )

    elif data == "mytickets":
        await query.edit_message_text(
            "🎫 არ გაქვთ ბილეთები",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 უკან", callback_data="back")]
            ])
        )

    # DEPOSIT
    elif data == "deposit":
        await query.message.delete()

        photo_url = "https://i.ibb.co/HfMcFZJ0/4935.jpg"

        text = f"""
❌ <b>არასაკმარისი ბალანსი</b>

💰 შეავსე ბალანსი

<code>{BTC_WALLET}</code>
"""

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 უკან", callback_data="back")]
            ])
        )

    elif data == "leads":
        keys = ["tier2", "tier1", "tool", "tlst"]
        await query.edit_message_text(
            "🎟️ ბილეთები",
            reply_markup=shop_menu()
        )

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = products[key]

        if balances[user_id] < item["price"]:
            await query.edit_message_text(
                f"{item['name']}\n{item['description']}\n💵 {item['price']}₾",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Deposit", callback_data="deposit")]
                ])
            )
            return

        balances[user_id] -= item["price"]

        await query.edit_message_text(
            f"✅ Bought {item['name']}\n💰 დარჩა {balances[user_id]}₾",
            reply_markup=main_menu()
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu))
    app.run_polling()


if __name__ == "__main__":
    main()
