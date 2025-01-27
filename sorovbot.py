from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

API_TOKEN = "7578409659:AAFxaAv8PKZgKAvaT-htK_JY8Lzlk8ZxeNQ"
CHANNEL_LINK = "https://t.me/fakt7_24"  # Kanal linki

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

# Admin ma'lumotlarini saqlash
admin_data = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    admin_data.clear()  # Avvalgi ma'lumotlarni tozalash
    await message.reply("Rasm yuboring.")

@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1].file_id
    admin_data["photo"] = photo
    await message.reply("Post uchun matnni kiriting.")

@dp.message(lambda message: "photo" in admin_data and "text" not in admin_data)
async def handle_text(message: types.Message):
    text = message.text
    admin_data["text"] = text

    # Post matnini interaktiv va stekirlar bilan yaratish
    formatted_text = (
        "🌟 Qiziqarli Faktlar 🌟\n\n"  # Bu birinchi qator
        f"{text}\n\n"  # Foydalanuvchidan olingan matn
        f"\n🔔 Kanalni kuzatib boring: {CHANNEL_LINK} 📚"  # Kanal havolasi
    )

    # Tayyor postni ko‘rsatish
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=admin_data["photo"],
        caption=formatted_text
    )
    await message.reply("Post tayyor!")
    admin_data.clear()  # Ma'lumotlarni tozalash

async def main():
    # Bot komandalarini ro'yxatdan o'tkazish
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Botni ishga tushirish")
    ])
    # Dispatcherni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
