# Telegram ChatGPT Bot

Bu loyiha oddiy Telegram bot bo'lib, OpenAI ChatGPT modeli orqali savollarga javob beradi.

## Kerakli narsalar

1. Python 3.9+\n2. Telegram bot token (BotFather dan)\n3. OpenAI API kaliti

## O'rnatish va ishga tushirish

```bash
git clone <repo_url>
cd telegram-chatgpt-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env faylida TELEGRAM_TOKEN va OPENAI_API_KEY ni to'ldiring
python main.py
