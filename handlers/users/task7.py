from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.task3_5_7_8_ikeyboard import get_concurs_name
from loader import dp, db
from states.Tasks_states import Task_7


@dp.message_handler(text="Завдання №7")
async def task7(message: types.Message):
    ikeyboard = await get_concurs_name()
    await message.answer("Виберіть Конкурс, переможців якого ви хочете побачити",
                         reply_markup=ikeyboard)
    await Task_7.task7.set()


@dp.callback_query_handler(state=Task_7.task7)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task7(call.data)
    await call.answer()
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Ім'я артиста: {record_data.get('participant_name')}</code>\n"
                                      f"<code>Конкурс: {record_data.get('concurs_name')}</code>\n"
                                      f"<code>Місце: {record_data.get('place')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №7 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №7 виконано</b>", parse_mode='html')

    await state.reset_state()
