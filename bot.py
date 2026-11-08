import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ==========================================
# AJMEER KHAN HACKER KING - TELEGRAM BOT
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8800135805:AAHaIZJBsRKbDFXVEYBrwZhKgg4K8mWzVk0")
BOT_NAME = "AJMEER KHAN HACKER KING"
DEVELOPER = "Ajmeer Khan"

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ==========================================
# START COMMAND
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("🤖 Bot Information", callback_data="about"),
            InlineKeyboardButton("👤 My Profile", callback_data="profile"),
        ],
        [
            InlineKeyboardButton("📋 Commands", callback_data="commands"),
            InlineKeyboardButton("⏰ Date & Time", callback_data="time"),
        ],
        [
            InlineKeyboardButton("⚡ Ping Bot", callback_data="ping"),
        ],
        [
            InlineKeyboardButton("🛠 Developer", callback_data="developer"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"👑 <b>WELCOME TO {BOT_NAME}</b>\n\n"
        f"🔥 Hello, {user.first_name}!\n\n"
        "🚀 Welcome to your professional Telegram bot.\n"
        "Choose an option from the menu below.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚡ <b>Status:</b> Online\n"
        "🤖 <b>Version:</b> 1.0.0\n"
        f"👑 <b>Developer:</b> {DEVELOPER}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "💎 Enjoy using the bot!"
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# HELP COMMAND
# ==========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📚 <b>BOT COMMANDS</b>\n\n"
        "🚀 /start - Start the bot\n"
        "📋 /help - Show commands\n"
        "ℹ️ /about - About the bot\n"
        "🆔 /id - Get your Telegram ID\n"
        "👤 /info - Your profile information\n"
        "⏰ /time - Current date and time\n"
        "⚡ /ping - Check bot response\n"
        "🔄 /menu - Open main menu\n\n"
        "👑 <b>AJMEER KHAN HACKER KING</b>"
    )

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# ABOUT COMMAND
# ==========================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🤖 <b>ABOUT THIS BOT</b>\n\n"
        "👑 Name: AJMEER KHAN HACKER KING\n"
        "⚙️ Platform: Telegram\n"
        "🐍 Language: Python\n"
        "📦 Library: python-telegram-bot\n"
        "🔥 Version: 1.0.0\n"
        "🟢 Status: Active\n\n"
        "💎 A professional Telegram bot "
        "designed for useful commands and interactive features."
    )

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# USER ID COMMAND
# ==========================================

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"🆔 <b>Your Telegram ID:</b>\n\n"
        f"<code>{user.id}</code>",
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# USER INFORMATION COMMAND
# ==========================================

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    username = f"@{user.username}" if user.username else "Not available"
    full_name = user.full_name or "Not available"

    message = (
        "👤 <b>YOUR PROFILE INFORMATION</b>\n\n"
        f"📝 <b>Name:</b> {full_name}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"🌐 <b>Language:</b> {user.language_code or 'Unknown'}\n"
        f"🤖 <b>Bot Account:</b> {'Yes' if user.is_bot else 'No'}"
    )

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# DATE AND TIME COMMAND
# ==========================================

async def current_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().astimezone()

    message = (
        "⏰ <b>DATE & TIME INFORMATION</b>\n\n"
        f"📅 Date: {now.strftime('%d-%m-%Y')}\n"
        f"🕒 Time: {now.strftime('%I:%M:%S %p')}\n"
        f"🌍 Timezone: {now.tzname() or 'Local'}"
    )

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# PING COMMAND
# ==========================================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = datetime.now()

    message = await update.message.reply_text("⚡ Checking bot status...")

    elapsed = (datetime.now() - start_time).total_seconds() * 1000

    await message.edit_text(
        "🟢 <b>BOT IS ONLINE!</b>\n\n"
        f"⚡ Response Time: {elapsed:.2f} ms\n"
        "🚀 Status: Operational\n"
        "👑 Powered by AJMEER KHAN",
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# MENU COMMAND
# ==========================================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🤖 About", callback_data="about"),
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
        ],
        [
            InlineKeyboardButton("📋 Commands", callback_data="commands"),
            InlineKeyboardButton("⏰ Time", callback_data="time"),
        ],
        [
            InlineKeyboardButton("⚡ Ping", callback_data="ping"),
            InlineKeyboardButton("🛠 Developer", callback_data="developer"),
        ],
    ]

    await update.message.reply_text(
        "👑 <b>MAIN MENU</b>\n\nSelect an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML,
    )


# ==========================================
# INLINE BUTTON HANDLER
# ==========================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    user = query.from_user
    data = query.data

    if data == "about":
        text = (
            "🤖 <b>ABOUT BOT</b>\n\n"
            "👑 AJMEER KHAN HACKER KING\n"
            "🐍 Python Telegram Bot\n"
            "🔥 Version: 1.0.0\n"
            "🟢 Status: Active"
        )
    elif data == "profile":
        username = f"@{user.username}" if user.username else "Not available"

        text = (
            "👤 <b>YOUR PROFILE</b>\n\n"
            f"📝 Name: {user.full_name}\n"
            f"🔗 Username: {username}\n"
            f"🆔 ID: <code>{user.id}</code>\n"
            f"🌐 Language: {user.language_code or 'Unknown'}"
        )
    elif data == "commands":
        text = (
            "📋 <b>AVAILABLE COMMANDS</b>\n\n"
            "/start - Start bot\n"
            "/help - Help menu\n"
            "/about - About bot\n"
            "/id - Telegram ID\n"
            "/info - User information\n"
            "/time - Date and time\n"
            "/ping - Bot status\n"
            "/menu - Main menu"
        )
    elif data == "time":
        now = datetime.now().astimezone()

        text = (
            "⏰ <b>DATE & TIME</b>\n\n"
            f"📅 {now.strftime('%d-%m-%Y')}\n"
            f"🕒 {now.strftime('%I:%M:%S %p')}\n"
            f"🌍 {now.tzname() or 'Local'}"
        )
    elif data == "ping":
        text = (
            "🟢 <b>BOT IS ONLINE!</b>\n\n"
            "⚡ Status: Operational\n"
            "🚀 Response: Active"
        )
    elif data == "developer":
        text = (
            "🛠 <b>DEVELOPER INFORMATION</b>\n\n"
            "👑 Developer: Ajmeer Khan\n"
            "🔥 Brand: AJMEER KHAN HACKER KING\n"
            "🐍 Language: Python"
        )
    elif data == "main_menu":
        keyboard = [
            [
                InlineKeyboardButton("🤖 About", callback_data="about"),
                InlineKeyboardButton("👤 Profile", callback_data="profile"),
            ],
            [
                InlineKeyboardButton("📋 Commands", callback_data="commands"),
                InlineKeyboardButton("⏰ Time", callback_data="time"),
            ],
            [
                InlineKeyboardButton("⚡ Ping", callback_data="ping"),
                InlineKeyboardButton("🛠 Developer", callback_data="developer"),
            ],
        ]
        await query.edit_message_text(
            "👑 <b>MAIN MENU</b>\n\nSelect an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML,
        )
        return
    else:
        text = "❌ Unknown option. Please try again."

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]),
    )


# ==========================================
# UNKNOWN COMMAND HANDLER
# ==========================================

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Unknown command!\n\n"
        "Use /help to see all available commands."
    )


# ==========================================
# ERROR HANDLER
# ==========================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("An exception occurred:", exc_info=context.error)


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError(
            "Please set your Telegram bot token using "
            "the BOT_TOKEN environment variable."
        )

    # Timeouts set to 30 seconds to prevent connection drops in Termux
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()
    )

    # Register commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("id", user_id))
    application.add_handler(CommandHandler("info", user_info))
    application.add_handler(CommandHandler("time", current_time))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("menu", menu))

    # Register inline buttons
    application.add_handler(CallbackQueryHandler(button_handler))

    # Unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Register error handler
    application.add_error_handler(error_handler)

    logger.info("%s is starting...", BOT_NAME)

    # Start bot
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


# ==========================================
# RUN BOT
# ==========================================

if __name__ == "__main__":
    main()
