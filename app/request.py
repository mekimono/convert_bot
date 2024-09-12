from aiogram import Router, F
from aiogram.filters import CommandStart, Command, ExceptionTypeFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.methods import get_file
import app.keyboard as kb
import aspose.words as aw
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from run import bot

router = Router()


class ConvertState(StatesGroup):
    file_id = State()
    file_format = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(ConvertState.file_id)
    await message.answer(f'Здравствуй, {message.from_user.username}, я бот для конвертации PDF файлов')
    await message.answer('Отправляйте файл, который хотите конвертировать')


@router.message(ConvertState.file_id, F.document)
async def convert_step1(message: Message, state: FSMContext):
    await state.update_data(file_id=message.document.file_id)
    await state.set_state(ConvertState.file_format)
    await message.answer('Выберите формат для конвертации', reply_markup=kb.keyboard_markup.as_markup())


@router.callback_query(ConvertState.file_format)
async def convert_step2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(file_format=callback.data)
    data = await state.get_data()
    await callback.message.answer(f'Форматируем в {callback.data} формат')

    file_id = data['file_id']
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'saved_files/{file_id}.pdf')
    docu = aw.Document(f'saved_files/{file_id}.pdf')
    docu.save(f'saved_files/{file_id}.{data["file_format"]}')
    await bot.send_document(callback.message.chat.id, document=FSInputFile(path=f'saved_files/{file_id}.{data["file_format"]}'))





