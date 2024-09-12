from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Конвертировать', callback_data='convert')]
])

keyboard_markup = InlineKeyboardBuilder()

format_types = {
    'DOCX': 'docx',
    'MD': 'md',
    'HTML': 'html',
    'TXT': 'txt',
    'DOC': 'doc',
    'EPUB': 'epub',
    'PNG': 'png',
    'RTF': 'rtf',
    'ODT': 'odt'
}

for key, value in format_types.items():
    keyboard_markup.button(text=f'{key}', callback_data=f'{value}')

keyboard_markup.adjust(3, 3)




