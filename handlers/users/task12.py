from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.Tasks_states import Task_12


@dp.message_handler(text="Завдання №12")
async def task6(message: types.Message):
    await message.answer("Введіть проміжок дат через пробіл(yyyy-mm-dd уууу-mm-dd)")
    await Task_12.task12.set()


@dp.message_handler(state=Task_12.task12)
async def catch_and_search(message: types.Message, state: FSMContext):
    min_event_date, max_event_date = message.text.split(" ")
    min_event_date = datetime.strptime(min_event_date, '%Y-%m-%d')
    max_event_date = datetime.strptime(max_event_date, '%Y-%m-%d')
    result = await db.task12(min_event_date, max_event_date)
    await message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await message.answer(f"<code>Місце: {record_data.get('location')}</code>\n"
                                 f"<code>Дата заходу: {record_data.get('date_of_event')}</code>\n"
                                 f"<code>Назва заходу: {record_data.get('event_name')}</code>\n",
                                 parse_mode='html')
        await message.answer("<b>Завдання №12 виконано</b>", parse_mode='html')
    else:
        await message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await message.answer("<b>Завдання №12 виконано</b>", parse_mode='html')

    await state.reset_state()
