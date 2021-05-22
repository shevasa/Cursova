from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import get_genres_ikeyboard
from loader import dp, db
from states import Task_1
from states.Task2 import Task_2


@dp.message_handler(text="Завдання №2")
async def start_task1(message: types.Message):
    ikeyboard = await get_genres_ikeyboard()
    await message.answer("Виконуємо <b>Завдання №2</b>\n"
                         "Артистів якого жанру знайти?", reply_markup=ikeyboard)
    await Task_2.task2.set()


@dp.callback_query_handler(state=Task_2.task2)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task2(call.data)
    await call.answer()
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Ім'я: {record_data.get('artist_name')}</code>\n"
                                      f"<code>Жанр: {record_data.get('genre')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №2 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №2 виконано</b>", parse_mode='html')

    await state.reset_state()
