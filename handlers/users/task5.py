from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.task3_5_7_8_ikeyboard import get_artists_names
from loader import dp, db
from states.Tasks_states import Task_5


@dp.message_handler(text="Завдання №5")
async def start_task1(message: types.Message):
    ikeyboard = await get_artists_names()
    await message.answer("Виконуємо <b>Завдання №5</b>\n"
                         "Імпрессаріо якого артиста знайти?", reply_markup=ikeyboard)
    await Task_5.task5.set()


@dp.callback_query_handler(state=Task_5.task5)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task5(call.data)
    await call.answer()
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Ім'я артиста: {record_data.get('artist_name')}</code>\n"
                                      f"<code>Імпрессаріо: {record_data.get('impressario_name')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №5 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №5 виконано</b>", parse_mode='html')

    await state.reset_state()
