import asyncio
from io import BytesIO

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.session import aiohttp
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, URLInputFile

from config import config

TELEGRAM_BOT_TOKEN = config.telegram_bot_token
BACKEND_BASE_URL = config.backend_base_url


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


class AddFriend(StatesGroup):
    photo = State()
    name = State()
    profession = State()
    profession_description = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Привіт! Я бот для друзів. Використовуй /friends щоб побачити всіх.")


@router.message(Command("friends"))
async def cmd_friends(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_BASE_URL}/friends/") as resp:
            if resp.status != 200:
                await message.reply("Помилка при отриманні друзів.")
                return
            data = await resp.json()
            friends = data.get("items", [])
            if not friends:
                await message.reply("Список друзів порожній.")
                return
            for friend in friends:
                text = f"Name:{friend['name']}\nProfession:{friend['profession']}\nDescription:{friend['profession_description']}\n"
                if friend.get("photo_url"):
                    try:
                        file = URLInputFile(friend.get("photo_url"))
                        await message.answer_photo(file, caption=text)
                    except Exception:
                        pass
                else:
                    await message.answer(text)


@router.message(Command("addfriend"))
async def start_add_friend(message: Message, state: FSMContext):
    await state.set_state(AddFriend.photo)
    await message.answer("📸 Надішли фото друга")


@router.message(AddFriend.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("Тепер введи ім’я 👇")
    await state.set_state(AddFriend.name)


@router.message(AddFriend.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Вкажи професію 💼")
    await state.set_state(AddFriend.profession)


@router.message(AddFriend.profession)
async def add_profession(message: Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer("Короткий опис 👇")
    await state.set_state(AddFriend.profession_description)


@router.message(AddFriend.profession_description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(profession_description=message.text)
    data = await state.get_data()

    file_info = await bot.get_file(data["photo"])
    file_path = file_info.file_path
    file_bytes = await bot.download_file(file_path)

    form = aiohttp.FormData()
    form.add_field("name", data["name"])
    form.add_field("profession", data["profession"])
    form.add_field("profession_description", data["profession_description"])
    form.add_field(
        "photo",
        BytesIO(file_bytes.read()),
        filename="photo.png",
        content_type="image/png"
    )
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND_BASE_URL}/friends/", data=form) as response:
            if response.status == 201:
                await message.answer("Друга створено!")
                await message.answer(await response.text())
            else:
                await message.answer("Error")


    await state.clear()


@router.message(Command("friend"))
async def get_friend_detail(message: Message, command: CommandObject):
    friend_id = command.args  # отримуємо <id> після /friend
    if not friend_id:
        await message.reply("❌ Будь ласка, вкажи ID друга: /friend <id>")
        return

    # робимо запит до бекенду
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_BASE_URL}/friends/{friend_id}") as resp:
            if resp.status != 200:
                await message.reply(f"❌ Друг з ID {friend_id} не знайдений.")
                return
            data = await resp.json()

    # Формуємо текст для повідомлення
    text = f"👤 Name: {data.get('name', '-')}\n" \
           f"💼 Profession: {data.get('profession', '-')}\n" \
           f"✍️ Description: {data.get('profession_description', '-')}"

    # Відправляємо повідомлення з фото, якщо воно є
    photo_url = data.get("photo_url")
    if photo_url:
        file = URLInputFile(photo_url)
        await message.answer_photo(file, caption=text)
    else:
        await message.answer(text)


@router.message(Command("askfriend"))
async def ask_friend(message: Message, command: CommandObject):
    friend_id = command.args
    if not friend_id:
        await message.reply("❌ Будь ласка, вкажи ID друга: /friend <id>")
        return
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND_BASE_URL}/friends/{friend_id}/ask/") as resp:
            data = await resp.json()
    text = data.get("generated_text")
    if len(text) > 100:
        await message.reply(text[:100])
    await message.reply(text)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
