from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.task3_5_7_8_ikeyboard import get_place_name
from loader import dp, db
from states.Tasks_states import Task_8


@dp.message_handler(text="Завдання №8")
async def task7(message: types.Message):
    ikeyboard = await get_place_name()
    await message.answer("Виберіть місце де шукати події",
                         reply_markup=ikeyboard)
    await Task_8.task8.set()


@dp.callback_query_handler(state=Task_8.task8)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    result = await db.task8(call.data)
    await call.answer()
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Назва події: {record_data.get('event_name')}</code>\n"
                                      f"<code>Місце: {record_data.get('place')}</code>\n",
                                      parse_mode='html')
        await call.message.answer("<b>Завдання №8 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №8 виконано</b>", parse_mode='html')

    await state.reset_state()
