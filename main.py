import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from openai import OpenAI
from dotenv import load_dotenv

# .env faylini yuklab olish
load_dotenv()

# Muhit o'zgaruvchilarini olish
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("TELEGRAM_TOKEN va OPENAI_API_KEY muhit o'zgaruvchilari aniqlanmadi!")

# Telegram va OpenAI mijozlari
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
client = OpenAI(api_key=OPENAI_API_KEY)

# Log sozlamalari
logging.basicConfig(level=logging.INFO)


# GPT'dan javob olish funksiyasi
async def get_gpt_answer(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # kerak bo'lsa gpt-4 yoki gpt-3.5 ham ishlatish mumkin
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content


# Start komandasi
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("👋 Salom! Men Anilordtv va Anifinx kanal uchun yaratilgan bot man.")


# Asosiy xabarlarni qayta ishlash
@dp.message_handler()
async def chat_handler(message: types.Message):
    try:
        user_text = message.text
        gpt_response = await get_gpt_answer(user_text)
        await message.answer(gpt_response)
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("❌ Xatolik yuz berdi. Keyinroq urinib ko'ring.")


if __name__ == "__main__":
    logging.info("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
