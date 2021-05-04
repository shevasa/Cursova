from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def get_impressarios_names():
    names = list(await db.get_impressarios_names())
    ikeyboard = InlineKeyboardMarkup(row_width=1)
    for record in names:
        button = InlineKeyboardButton(text=f'{record.get("name")}',
                                      callback_data=f'{record.get("name")}')
        ikeyboard.insert(button)
    return ikeyboard
