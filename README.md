# 📝 Telegram Notion Note Bot

A Telegram bot that saves your notes to both a local SQLite database and Notion — instantly, with a simple command.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- Save notes from Telegram directly to **Notion database**
- Backup copy saved in **local SQLite database**
- Simple commands — just type `/note your text`
- Fast and lightweight

---

## 📋 Requirements

- Python 3.10+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Notion Integration Token
- Notion Database ID

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-notion-bot.git
cd telegram-notion-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy the example file:

```bash
cp .env.example .env
```

Then open `.env` and fill in your values:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
```

### 4. Notion Setup

1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Create a new integration → copy the **Internal Integration Token**
3. Create a Notion database with a column named **"Note"**
4. Open the database as full page → copy the ID from the URL
5. In your database, click `...` → **Connections** → add your integration

### 5. Run the bot

```bash
python bot.py
```

---

## 🤖 Bot Commands

| Command | Description |
|--------|-------------|
| `/start` | Start the bot |
| `/note <text>` | Save a note to Notion + local DB |

**Example:**
```
/note Buy milk from the store
/note Meeting at 3pm tomorrow
/note Important idea: build a rocket
```

---

## 📁 Project Structure

```
telegram-notion-bot/
├── bot.py            # Main bot code
├── .env              # Secret tokens (never upload!)
├── .env.example      # Template for .env
├── .gitignore        # Ignores .env and notes.db
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🔒 Security Notes

> **Never upload your `.env` file to GitHub!**  
> The `.gitignore` already protects you — but double check before pushing.

- Regenerate tokens immediately if accidentally exposed
- Telegram: BotFather → `/mybots` → Revoke token
- Notion: notion.so/my-integrations → Regenerate

---

## 🌐 Note for Pakistan Users

Telegram API may be blocked. Use a VPN (e.g., [Cloudflare WARP](https://one.one.one.one)) before running the bot.

---

## 📄 License

MIT License — free to use and modify.

---

*Built with ❤️ using python-telegram-bot & Notion API*
