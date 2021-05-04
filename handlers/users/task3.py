from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.task3_ikeyboard import get_impressarios_names
from loader import dp, db
from states.Tasks_states import Task_3


@dp.message_handler(text="Завдання №3")
async def start_task1(message: types.Message):
    ikeyboard = await get_impressarios_names()
    await message.answer("Виконуємо <b>Завдання №3</b>"
                         "Артистів якого жанру знайти?", reply_markup=ikeyboard)
    await Task_3.task3.set()


@dp.callback_query_handler(state=Task_3.task3)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task3(call.data)
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Ім'я артиста: {record_data.get('artist_name')}</code>\n"
                                      f"<code>Імпрессаріо: {record_data.get('impressario_name')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №3 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №3 виконано</b>", parse_mode='html')

    await state.reset_state()
