import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram import filters
import keyboard as kb
from config import TOKEN
import aspose.words as aw
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


bot = Bot(token=TOKEN)
dp = Dispatcher()


# class StatesGroup является классом состояний необходимых для хранения информации
# создавая экземпляры основываясь на том, какую информацию мы хотим хранить

class ConvertState(StatesGroup):
    # ID файла нам необходимо, чтобы скачать данный файл на носитель
    file_id = State()
    # А так же формат файла, чтобы понимать в какой формат пользователь хочет форматировать
    file_format = State()


@dp.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext):
    """ Приветствие и установка первого состояния считывания информации """

    await state.set_state(ConvertState.file_id)
    await message.answer(f'Здравствуй, {message.from_user.username}, я бот для конвертации PDF файлов')
    await message.answer('Отправляйте файл, который хотите конвертировать')


@dp.message(ConvertState.file_id, F.document)
async def convert_step1(message: types.Message, state: FSMContext):
    """ Получения документа от пользователя и внесение его в машину состояний """

    await state.update_data(file_id=message.document.file_id)
    await state.set_state(ConvertState.file_format)
    await message.answer('Выберите формат для конвертации', reply_markup=kb.keyboard_markup.as_markup())


@dp.callback_query(ConvertState.file_format)
async def convert_step2(callback: types.CallbackQuery, state: FSMContext):
    """ Считывание информации с callback данных и внесение их в машину состояний, в следствии - конвертация """

    await state.update_data(file_format=callback.data)
    data = await state.get_data()
    await callback.message.answer(f'Форматируем в .{callback.data} формат, это займет какое-то время')
    await callback.answer('')

    # Мы считываем ID файла, этой информации достаточно, чтобы сохранить файл себе на носитель
    # Далее используя библиотеку aspose-words мы конвертируем в тот формат, который мы получили
    # посредством callback данных

    file_id = data['file_id']
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f'saved_files/{file_id}.pdf')

    docu = aw.Document(f'saved_files/{file_id}.pdf')
    docu.save(f'saved_files/{file_id}.{data["file_format"]}')
    await bot.send_document(callback.message.chat.id,
                            document=types.FSInputFile(path=f'saved_files/{file_id}.{data["file_format"]}'))

    # Очистка данных состояния после конвертации

    await state.clear()


@dp.message(F.text)
async def text_message(message: types.Message):
    """ Реакция бота на текстовые сообщения """

    await message.answer('Я конвертирую PDF файлы, если вы хотите их конвертировать введите команду /start')


async def main():
    """ Игнорирует все апдейты пока бот находится в отключенном состоянии и запускает процесс """

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


#  Точка входа
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


