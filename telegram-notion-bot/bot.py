import os
import logging
import sqlite3
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- Setup ---
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Database (SQLite) ---
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sqlite(user_id, text):
    try:
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", (user_id, text))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"SQLite Error: {e}")
        return False

# --- Notion API ---
def push_to_notion(text):
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return None

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Note": {
                "title": [
                    {"text": {"content": text}}
                ]
            }
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            logging.error(f"Notion Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Notion Connection Failed: {e}")
        return False

# --- Bot Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Notion Bot Ready!**\n\n"
        "Type `/note <your text>` to save a note."
    )

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    content = ' '.join(context.args)

    if not content:
        await update.message.reply_text("⚠️ Usage: `/note Buy milk`")
        return

    # 1. Save Local
    db_saved = save_to_sqlite(user_id, content)

    # 2. Save Notion
    notion_status = ""
    if NOTION_TOKEN and NOTION_DB_ID:
        if push_to_notion(content):
            notion_status = " + 📝 Notion"
        else:
            notion_status = " (Notion Failed)"

    if db_saved:
        await update.message.reply_text(f"✅ Saved{notion_status}!")
    else:
        await update.message.reply_text("❌ Database Error.")

# --- Run ---
if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN missing from .env")
        exit(1)

    init_db()
    print("Bot is running...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('note', note))

    app.run_polling()
