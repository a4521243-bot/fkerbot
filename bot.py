from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8721950488

users = set()
balances = {}

BTC_WALLET = "17hQJ4sGmt4yMniMfAfjEgRvAPPCnycfdc"


# =========================
# PRODUCTS (UPDATED LUXURY TOURS & EVENTS)
# =========================
products = {
# ALLPRODUCTS
    "tier2": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 270,
        "description":"სთეიჯი: Tier#2 - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026"
    },
        "tier1": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 320,
        "description":"სთეიჯი: Tier#1 - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026"
    },
    "tool": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price": 500, 
        "description":"სთეიჯი: Orbit - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026"
    },
    "tlst": {
        "name": "YE LIVE DINAMO/KANYE WEST",
        "price":1500,
        "description":"სთეიჯი: VIP - ხელმისაწვდომია✅\n📅თარიღი: 12 ივნისი, 2026"
    },
    "crc": {
        "name": "💳Usable credit cards",
        "price":1000,
        "description":"🌍From: 🇩🇪\n🟥Limit: 4000💶"
    },
    "trc": {
        "name": "💳Usable credit cards",
        "price":500,
        "description":"🌍From: 🇩🇪\n🟥Limit: 2000💶"
    },
}


# =========================
# MENUS
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 ვიტრინა", callback_data="shop")],
        [InlineKeyboardButton("💰 ბალანსი", callback_data="balance")],
        [InlineKeyboardButton("🔐 ადმინი", callback_data="admin")]
    ])


def shop_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎟️ ბილეთები", callback_data="leads")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])


def product_menu(keys, back="shop"):
    keyboard = []
    for k in keys:
        p = products[k]
        # Show description if available
        text = f"{p['name']} - ₾{p['price']}"
        if "description" in p:
            text += f"\n{p['description']}"
        keyboard.append([InlineKeyboardButton(text, callback_data=f"buy_{k}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back)])
    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    if user_id not in balances:
        balances[user_id] = 0

    text = "იჩქარეთ 🎟️🔥"

    # GIF გაგზავნა
    msg = await context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation="https://www.bloggif.com/tmp/00819beaf174f80fcfefa2f524fdf244/text.gif",
        caption="."
    )

    # ანიმაციური ტექსტი
    for i in range(1, len(text) + 1):
        await asyncio.sleep(0.3)

        try:
            await msg.edit_caption(
                caption=text[:i]
            )
        except:
            pass

    # მთავარი მესიჯი
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
👋 ჰეი, კეთილი იყოს თქვენი მობრძანება!

აქ შეგიძლია სწრაფად და უსაფრთხოდ შეიძინო ბილეთები 🎉

🎟️ აირჩიე ღონისძიება
💳 გადაიხადე კრიპტოთი
📩 მიიღე ბილეთი პირდაპირ ტელეგრამში

ადმინისტრატორი @tktgeassist

დაიწყე ახლავე 👇
""",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# =========================
# CALLBACK (SIMPLE ROUTER)
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_id not in balances:
        balances[user_id] = 0

    # BACK
    if data == "back":
        await query.edit_message_text(
    """
     🏠 <b>მთავარი მენიუ</b> 🏠
     
🎟️ აირჩიე ღონისძიება
💳 გადაიხადე კრიპტოთი
📩 მიიღე ბილეთი პირდაპირ ტელეგრამში
ადმინისტრატორი @tktgeassist

დაიწყე ახლავე 👇

""",
    parse_mode="HTML",
    reply_markup=main_menu()
)

    # SHOP
    elif data == "shop":
        await query.edit_message_text(
    """
    🛒 <b>ვიტრინა</b>
    
აირჩიე სასურველი 👇
""",
    parse_mode="HTML",
    reply_markup=shop_menu()
)

    # BALANCE
    elif data == "balance":
        await query.edit_message_text(
            f"💰 ბალანსი: ₾{balances[user_id]}",
            reply_markup=main_menu()
        )

    # DEPOSIT
    elif data == "deposit":
        await query.edit_message_text(
    f"""
❌ <b>არასაკმარისი ბალანსი</b>

💰 <b>საჭიროა შევსება</b>

გასაგრძელებლად გაგზავნე BTC შემდეგ მისამართზე:

<code>{BTC_WALLET}</code>

⚡ გადახდის შემდეგ, ბალანსი ავტომატურად განახლდება.
🔒 უსაფრთხო ბლოკჩეინ ტრანზაქცია

""",
    parse_mode="HTML",
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])
)

    # CATEGORIES
    elif data == "leads":
        keys = ["tier2", "tier1", "tool", "tlst"]
        await query.edit_message_text(
    """
🎟️ <b>ბილეთები</b> 🎟️

აირჩიე სასურველი 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "cards":
        keys = ["crc", "trc"]
        await query.edit_message_text(
    """
💳 <b>Credit Cards</b> 💳

🫶 Support: @luxchainsupport

Choose your tour below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "events":
        keys = ["cannes", "monaco_f1"]
        await query.edit_message_text(
    """
🎫 <b>Exclusive Events</b> 🎫

🫶 Support: @luxchainsupport

Choose your event below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    elif data == "voip":
        keys = ["vip", "tool"]
        await query.edit_message_text(
    """
💻 <b>Elite Services</b> 💻

🫶 Support: @luxchainsupport

Choose a service below 👇
""",
    parse_mode="HTML",
    reply_markup=product_menu(keys)
)

    # BUY
    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        item = products[key]

        if balances[user_id] < item["price"]:
            await query.edit_message_text(
                f"{item['name']}\n"
                f"{item['description']}\n"
                f"💵ფასი : {item['price']}₾\n"
                f"💰ბალანსი : {balances[user_id]}₾",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ შეძენა", callback_data="deposit")],
                    [InlineKeyboardButton("🔙 უკან", callback_data="shop")]
                ])
            )
            return

        balances[user_id] -= item["price"]

        await query.edit_message_text(
            f"✅ Bought: {item['name']}\n"
            f"Remaining: ${balances[user_id]}",
            reply_markup=main_menu()
        )

    # ADMIN
    elif data == "admin":
        if user_id != ADMIN_ID:
            await query.answer("არხარ ადმინისტრატორი ❌", show_alert=True)
            return

        await query.edit_message_text(
            f"🔐 Admin panel\nUsers: {len(users)}\nProducts: {len(products)}",
            reply_markup=main_menu()
        )
        
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(CallbackQueryHandler(menu))

    app.run_polling()


if __name__ == "__main__":
    main()
