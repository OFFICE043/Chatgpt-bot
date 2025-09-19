# main.py
# Bot uchun asosiy fayl

import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

# Muhim: Foydalanuvchi interfeysidagi barcha matnlar O'ZBEK (latın) tilida yozilgan

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ADMIN_IDS = os.getenv('ADMIN_IDS', '')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("TELEGRAM_TOKEN va OPENAI_API_KEY muhit o'zgaruvchilari aniqlanmadi. .env faylini tekshiring.")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# rules.txt faylidan qoidalarni yuklaymiz
with open('rules.txt', 'r', encoding='utf-8') as f:
    BOT_QOIDALARI = f.read().strip()

# Boshlang'ich xabar
START_XABAR = (
    "Assalomu alaykum! Men ChatGPT asosidagi yordamchim.\n"
    "Savolingizni yozing — men O'zbek (lotin) tilida javob beraman.\n\n"
    "Agar kod kerak bo'lsa, aniq til va tafsilotlarni ayting.\n"
)

@dp.message_handler(commands=['start'])
async def boshla(message: types.Message):
    await message.reply(START_XABAR)

@dp.message_handler(commands=['help'])
async def yordam(message: types.Message):
    yordam_matn = (
        "Qo'llanma:\n"
        "/start - botni ishga tushirish\n"
        "/help - yordam\n"
        "Faqat oddiy savollar va kod so'rovlarini qabul qilaman.\n"
    )
    await message.reply(yordam_matn)

async def chatgpt_sozla(savol: str) -> str:
    """Savol va qoidalarni OpenAI ChatCompletion-ga yuboradi va javobni qaytaradi"""
    prompt = f"{BOT_QOIDALARI}\n\nFoydalanuvchi savoli:\n{savol}"

    # openai.ChatCompletion sync funksiyasini bloklamaslik uchun asyncio.to_thread ishlatamiz
    def _call_openai():
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # agar sizda mavjud bo'lmasa modelni 'gpt-3.5-turbo' ga almashtiring
            messages=[
                {"role": "system", "content": BOT_QOIDALARI},
                {"role": "user", "content": savol}
            ],
            max_tokens=1200,
            temperature=0.2,
        )
        return response

    try:
        resp = await asyncio.to_thread(_call_openai)
        text = resp['choices'][0]['message']['content'].strip()
        return text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

@dp.message_handler()
async def umumiy(message: types.Message):
    # Qisqa typing holatini ko'rsatish
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)

    foydalanuvchi_text = message.text
    javob = await chatgpt_sozla(foydalanuvchi_text)

    # Agar javob juda uzun bo'lsa bo'lib yuborish mumkin
    if len(javob) > 4000:
        # uzun javobni bo'lib yuborish
        for i in range(0, len(javob), 4000):
            await message.reply(javob[i:i+4000])
    else:
        await message.reply(javob)

if __name__ == '__main__':
    print("Bot ishga tushmoqda...")
    executor.start_polling(dp, skip_updates=True)
