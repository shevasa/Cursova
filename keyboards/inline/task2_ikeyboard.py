from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def get_genres_ikeyboard():
    genres = await db.get_genres()
    all_genres = list(record for record in genres)
    ikeyboard = InlineKeyboardMarkup(row_width=2)
    for record in all_genres:
        genre_name = record.get('name')
        button = InlineKeyboardButton(text=f'{genre_name}',
                                      callback_data=f'{genre_name}')
        ikeyboard.insert(button)
    return ikeyboard
