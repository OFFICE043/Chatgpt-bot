import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from openai import OpenAI
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

# Muhit o'zgaruvchilarini olamiz
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("TELEGRAM_TOKEN va OPENAI_API_KEY muhit o'zgaruvchilari aniqlanmadi!")

# Telegram va OpenAI mijozlarini sozlaymiz
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
client = OpenAI(api_key=OPENAI_API_KEY)

# Logging yoqamiz
logging.basicConfig(level=logging.INFO)


# /start komandasi
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Salom! Men ChatGPT bilan ishlaydigan botman 🤖\nSavolingizni yozing.")


# Barcha matnlarni OpenAI ga yuboramiz
@dp.message_handler()
async def chat_handler(message: types.Message):
    try:
        # OpenAI API orqali javob olish
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Tez va arzon model
            messages=[
                {"role": "system", "content": "Siz foydalanuvchiga yordam beradigan yordamchisiz."},
                {"role": "user", "content": message.text},
            ],
        )

        reply_text = completion.choices[0].message.content
        await message.answer(reply_text)

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Kechirasiz, serverda xatolik yuz berdi ❌")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
