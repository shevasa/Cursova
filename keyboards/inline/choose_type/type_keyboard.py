from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.choose_type.type_callback_data import type_callback

type_variants = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Театр", callback_data=type_callback.new(type="Театр")),
        InlineKeyboardButton(text="Концертний майданчик", callback_data=type_callback.new(type="Концертний майданчик"))
    ],
    [
        InlineKeyboardButton(text="Палац культури", callback_data=type_callback.new(type="Палац культури")),
        InlineKeyboardButton(text="Стадіон", callback_data=type_callback.new(type="Стадіон"))
    ]
])