from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import get_genres_ikeyboard
from loader import dp, db
from states.Tasks_states import Task_9


@dp.message_handler(text="Завдання №9")
async def task9(message: types.Message):
    ikeyboard = await get_genres_ikeyboard()
    await message.answer("Виконуємо <b>Завдання №9</b>"
                         "Імпрессаріо якого жанру знайти?", reply_markup=ikeyboard)
    await Task_9.task9.set()


@dp.callback_query_handler(state=Task_9.task9)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task9(call.data)
    await call.answer()
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Імпрессаріо: {record_data.get('impressario')}</code>\n"
                                      f"<code>Жанр: {record_data.get('genre')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №9 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №9 виконано</b>", parse_mode='html')

    await state.reset_state()