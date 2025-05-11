import os
import tempfile
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from app.generate import ai_generate


router = Router()


class Gen(StatesGroup):
    wait = State()
    pic_wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Бот работает')

@router.message(Command('pic'))
async def cmd_pic(message: Message, state: FSMContext):
    await message.answer('Отправьте, пожалуйста, картинку')
    await state.set_state(Gen.pic_wait)

@router.message(Gen.pic_wait, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING)

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        await message.bot.download_file(file.file_path, temp_file.name)
        temp_file_path = temp_file.name

    try:
        response = await ai_generate("", temp_file_path)
        await message.answer(response, parse_mode='Markdown')
    finally:
        os.unlink(temp_file_path)

    await state.clear()

@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Подождите, ответ генерируется')

@router.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    response =  await ai_generate(message.text)
    await message.answer(response, parse_mode='Markdown')
    await state.clear()
