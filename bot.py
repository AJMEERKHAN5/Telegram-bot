
import os
import io
import json
import uuid
import base64
import zipfile
import logging
import asyncio
import urllib.request
import urllib.error

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================================
# AJMEER KHAN HACKER KING
# AUTOMATIC APK BUILDER
# ==========================================

BOT_TOKEN = os.environ["8851145300:AAF2GmY9jk-TXO-gYd-GSx6wL1_ph90YmP4"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

GITHUB_OWNER = os.environ["GITHUB_OWNER"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

# Optional: comma-separated Telegram user IDs
ALLOWED_USERS = {
    int(x.strip())
    for x in os.getenv("ALLOWED_USERS", "").split(",")
    if x.strip()
}

MAX_FILE_SIZE = 20 * 1024 * 1024

API = "https://api.github.com"
WORKFLOW = "build-apk.yml"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def authorized(user_id):
    return not ALLOWED_USERS or user_id in ALLOWED_USERS


def github_request(method, endpoint, data=None):
    url = API + endpoint

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Ajmeer-Apk-Builder",
    }

    body = None

    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = response.read()

            if result:
                return json.loads(result.decode("utf-8"))

            return {}

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub error {error.code}: {details[:1000]}"
        ) from error


def upload_to_github(path, content):
    encoded = base64.b64encode(content).decode("ascii")

    endpoint = (
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/contents/{path}"
    )

    return github_request(
        "PUT",
        endpoint,
        {
            "message": f"Upload APK build input: {path}",
            "content": encoded,
            "branch": GITHUB_BRANCH,
        },
    )


def trigger_workflow(archive_path):
    endpoint = (
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/actions/workflows/{WORKFLOW}/dispatches"
    )

    github_request(
        "POST",
        endpoint,
        {
            "ref": GITHUB_BRANCH,
            "inputs": {
                "archive_path": archive_path,
            },
        },
    )


def validate_zip(data):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()

            if len(entries) > 500:
                raise ValueError("Too many files in ZIP.")

            total_size = 0

            for item in entries:
                name = item.filename.replace("\\", "/")

                if (
                    name.startswith("/")
                    or ".." in name.split("/")
                    or "\x00" in name
                ):
                    raise ValueError("Unsafe ZIP file path.")

                if item.file_size > MAX_FILE_SIZE:
                    raise ValueError("A ZIP entry is too large.")

                total_size += item.file_size

                if total_size > 100 * 1024 * 1024:
                    raise ValueError("Extracted ZIP is too large.")

                if item.flag_bits & 0x1:
                    raise ValueError("Encrypted ZIP files are unsupported.")

                if item.file_size > 0:
                    if item.compress_size == 0:
                        raise ValueError("Invalid ZIP entry.")

                    if item.file_size > item.compress_size * 100:
                        raise ValueError("Suspicious compression ratio.")

    except zipfile.BadZipFile as error:
        raise ValueError("Invalid ZIP file.") from error


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 AJMEER KHAN HACKER KING\n\n"
        "Welcome to Automatic APK Builder!\n\n"
        "📤 Send an HTML, PHP or ZIP project.\n"
        "⚙️ GitHub Actions will build your APK.\n\n"
        "Commands:\n"
        "/start - Start bot\n"
        "/apk - APK builder information\n"
        "/help - Help"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📱 APK BUILDER HELP\n\n"
        "Supported files:\n"
        "• .html\n"
        "• .php\n"
        "• .zip\n\n"
        "For a ZIP project, include index.html.\n"
        "PHP needs a hosted PHP server to execute.\n\n"
        "Maximum upload: 20 MB."
    )


async def apk_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "⚡ AUTOMATIC APK BUILDER\n\n"
        "1. Upload your website file.\n"
        "2. Wait for GitHub Actions.\n"
        "3. Open the build link.\n"
        "4. Download the APK artifact.\n\n"
        "Supported: HTML / PHP / ZIP."
    )


async def process_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    message = update.message

    if not authorized(user.id):
        await message.reply_text("⛔ You are not authorized.")
        return

    document = message.document

    if not document:
        return

    filename = document.file_name or "website.html"
    extension = os.path.splitext(filename)[1].lower()

    if extension not in (".html", ".php", ".zip"):
        await message.reply_text(
            "❌ Unsupported file.\n"
            "Upload HTML, PHP or ZIP."
        )
        return

    if document.file_size and document.file_size > MAX_FILE_SIZE:
        await message.reply_text("❌ Maximum file size is 20 MB.")
        return

    status = await message.reply_text(
        "⏳ Downloading your project..."
    )

    try:
        telegram_file = await context.bot.get_file(document.file_id)

        data = await telegram_file.download_as_bytearray()
        data = bytes(data)

        if len(data) > MAX_FILE_SIZE:
            raise ValueError("File exceeds the 20 MB limit.")

        if extension == ".zip":
            validate_zip(data)

        job_id = uuid.uuid4().hex[:12]

        safe_extension = extension
        archive_path = f"builds/{job_id}{safe_extension}"

        await status.edit_text(
            "📤 Uploading project to GitHub..."
        )

        await asyncio.to_thread(
            upload_to_github,
            archive_path,
            data
        )

        await status.edit_text(
            "🚀 Starting GitHub Actions..."
        )

        await asyncio.to_thread(
            trigger_workflow,
            archive_path
        )

        run_url = (
            f"https://github.com/{GITHUB_OWNER}/"
            f"{GITHUB_REPO}/actions"
        )

        await status.edit_text(
            "✅ BUILD STARTED SUCCESSFULLY!\n\n"
            f"🆔 Build ID: {job_id}\n"
            f"📁 File: {filename}\n\n"
            "⚙️ Your APK is being compiled.\n\n"
            "📦 Open GitHub Actions to check progress "
            "and download the APK artifact:\n"
            f"{run_url}\n\n"
            "👑 AJMEER KHAN HACKER KING"
        )

    except Exception as error:
        logger.exception("APK build submission failed")

        await status.edit_text(
            "❌ BUILD SUBMISSION FAILED\n\n"
            f"Reason: {str(error)[:700]}"
        )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.exception(
        "Telegram bot error",
        exc_info=context.error
    )


def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("apk", apk_command))

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            process_file
        )
    )

    app.add_error_handler(error_handler)

    logger.info("Ajmeer APK Builder started.")

    app.run_polling()


if __name__ == "__main__":
    main()
