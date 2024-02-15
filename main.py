from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from keyboards import keyboard
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.types import InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

class Form(StatesGroup):
    number = State()

    
@dp.message(CommandStart())
async def command_start_handler(message: Message,  state: FSMContext) -> None:
    await state.set_state(Form.number)
    await state.update_data(number=1)
    photo = FSInputFile(f"images/1.png")
    await message.answer_photo(photo, reply_markup=keyboard())

@dp.callback_query(F.data.in_(["prev","next"]))
async def nav_query(callback:CallbackQuery,  state: FSMContext)-> None:
    data = await state.get_data()
    text = data.get("number")
    try:
        text = int(text)
        if callback.data == "prev":
            text -= 1
        else:
            text += 1
        if text>3:
            text = 1
        if text < 1:
            text = 3
            

        await state.update_data(number=text)
        photo = FSInputFile(f"images/{text}.png")
        photo = InputMediaPhoto(media=photo)

        await callback.message.edit_media(photo,  reply_markup=keyboard())
    except Exception as e:
        logging.exception(str(e))



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())