# 🎞 Telegram GIF Maker Bot

A Telegram bot that converts a sequence of images into an animated GIF.  
Built with **python-telegram-bot** and **Pillow**, deployed on **Render** as a background worker.

---

## ✨ Features

- Upload 2–20 images and get back an animated GIF
- Choose frame speed: Slow / Normal / Fast / Very Fast
- Supports JPG, PNG, WEBP (sent as photos or document files)
- Auto-resizes frames to a consistent size
- Clean session management per user
- Hosted on GitHub, deployed on Render (free tier)

---

## 📂 Project Structure

```
telegram-gif-bot/
├── bot.py              # Telegram bot logic (ConversationHandler)
├── gif_maker.py        # Core GIF creation with Pillow
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config (background worker)
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repo

```bash
git clone https://github.com/<YOUR_USERNAME>/telegram-gif-bot.git
cd telegram-gif-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your bot token

Create a `.env` file (never commit this!):

```bash
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
```

Then export it:

```bash
export TELEGRAM_BOT_TOKEN=your_token_here   # Mac/Linux
set TELEGRAM_BOT_TOKEN=your_token_here      # Windows CMD
```

> Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

### 5. Run the bot

```bash
python bot.py
```

---

## ☁️ Deploy on Render (Background Worker)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/telegram-gif-bot.git
git push -u origin main
```

### Step 2 — Create a Render service

1. Go to [render.com](https://render.com) and log in
2. Click **New → Background Worker**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` — or configure manually:

| Setting | Value |
|---|---|
| **Environment** | Python |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

### Step 3 — Set environment variables

In the Render dashboard → your service → **Environment**:

| Key | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | `your_token_here` |

### Step 4 — Deploy

Click **Deploy**. Render will build and start your bot. It runs 24/7 as a background worker (no HTTP server needed).

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/makegif` | Start a new GIF session |
| `/done` | Finalize and generate the GIF |
| `/cancel` | Cancel the current session |
| `/help` | Show help |

---

## ⚙️ Configuration

Frame speed options (chosen via inline keyboard after `/done`):

| Option | Duration per frame |
|---|---|
| 🐢 Slow | 1000 ms |
| 🚶 Normal | 500 ms |
| 🏃 Fast | 200 ms |
| ⚡ Very Fast | 100 ms |

---

## 🛠 Tech Stack

- [python-telegram-bot v21](https://python-telegram-bot.org/) — Bot framework
- [Pillow](https://pillow.readthedocs.io/) — Image processing & GIF creation
- [Render](https://render.com) — Cloud deployment (background worker)
- [GitHub Actions](https://github.com/features/actions) — CI/CD

---

## 📄 License

MIT
