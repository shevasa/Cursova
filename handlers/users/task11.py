from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.Tasks_states import Task_11


@dp.message_handler(text="Завдання №11")
async def task6(message: types.Message):
    await message.answer("Введіть проміжок дат через пробіл(yyyy-mm-dd уууу-mm-dd)")
    await Task_11.task11.set()


@dp.message_handler(state=Task_11.task11)
async def catch_and_search(message: types.Message, state: FSMContext):
    min_event_date, max_event_date = message.text.split(" ")
    min_event_date = datetime.strptime(min_event_date, '%Y-%m-%d')
    max_event_date = datetime.strptime(max_event_date, '%Y-%m-%d')
    result = await db.task11(min_event_date, max_event_date)
    await message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await message.answer(f"<code>Організатор: {record_data.get('organizator')}</code>\n"
                                 f"<code>Кількість заходів: {record_data.get('number_of_events')}</code>\n",
                                 parse_mode='html')
        await message.answer("<b>Завдання №11 виконано</b>", parse_mode='html')
    else:
        await message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await message.answer("<b>Завдання №11 виконано</b>", parse_mode='html')

    await state.reset_state()