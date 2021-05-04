from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.choose_criteria.criteria_callback_data import criteria

choose_criteria_ikeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вибрати тип споруди", callback_data=criteria.new(name_of_criteria="type")),
        InlineKeyboardButton(text="Вибрати місткість", callback_data=criteria.new(name_of_criteria="number_of_seats"))
    ],
    [
        InlineKeyboardButton(text="Вхід безкоштовний?", callback_data=criteria.new(name_of_criteria="free")),
        InlineKeyboardButton(text="Під відкритим небом?", callback_data=criteria.new(name_of_criteria="open_air"))
    ],
    [
        InlineKeyboardButton(text="Знайти", callback_data=criteria.new(name_of_criteria="search"))
    ]
])