import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db
from states.Tasks_states import Task_6
from datetime import datetime


@dp.message_handler(text="Завдання №6")
async def task6(message: types.Message):
    await message.answer("Введіть проміжок дат через пробіл(yyyy-mm-dd уууу-mm-dd)")
    await Task_6.task6.set()


@dp.message_handler(state=Task_6.task6)
async def full_or_not(message: types.Message, state: FSMContext):
    await state.update_data({
        "date": message.text
    })
    await message.answer(f"Ви ввели такий проміжок часу <code>{message.text}</code>\n"
                         f"Виконати розширений пошук?(вивести всю інформацію про подію)",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [
                                 InlineKeyboardButton(text="Розширений пошук", callback_data="true")
                             ],
                             [
                                 InlineKeyboardButton(text="Нерозширений пошук", callback_data="false")
                             ]
                         ]))
    await Task_6.search.set()


@dp.callback_query_handler(state=Task_6.search)
async def catch_and_search(call: types.CallbackQuery, state: FSMContext):
    dates = await state.get_data("date")
    await call.answer()
    min_event_date, max_event_date = dates.get("date").split(" ")
    min_event_date = datetime.strptime(min_event_date, '%Y-%m-%d')
    max_event_date = datetime.strptime(max_event_date, '%Y-%m-%d')
    result = await db.task6(min_event_date,max_event_date)
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    logging.info(f"{call.data}")
    if result:
        for record in result:
            record_data = dict(record)
            if call.data == "true":
                await call.message.answer(f"<code>Назва події: {record_data.get('event_name')}</code>\n"
                                          f"<code>Дата події: {record_data.get('date')}</code>\n"
                                          f"<code>Тип події: {record_data.get('type_of-event')}</code>\n"
                                          f"<code>Місце: {record_data.get('place')}</code>\n"
                                          f"<code>Організатор: {record_data.get('organizator')}</code>\n",
                                          parse_mode='html')
            elif call.data == "false":
                await call.message.answer(f"<code>Назва події: {record_data.get('event_name')}</code>\n"
                                          f"<code>Дата події: {record_data.get('date')}</code>\n"
                                          f"<code>Організатор: {record_data.get('organizator')}</code>\n",
                                          parse_mode='html')
        await call.message.answer("<b>Завдання №6 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №6 виконано</b>", parse_mode='html')

    await state.reset_state()
