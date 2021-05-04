import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import choose_criteria_ikeyboard, criteria
from keyboards.inline.choose_type.type_keyboard import type_variants
from loader import dp, db
from states import Task_1


@dp.message_handler(text="Завдання №1")
async def start_task1(message: types.Message):
    await message.answer("Виконуємо <b>Завдання №1</b>", reply_markup=choose_criteria_ikeyboard)
    await Task_1.task_1.set()


@dp.callback_query_handler(criteria.filter(name_of_criteria="type"), state=Task_1.task_1)
async def choose_type(call: types.CallbackQuery):
    await call.message.answer("Виберіть тип споруди", reply_markup=type_variants)
    await Task_1.type.set()


@dp.callback_query_handler(state=Task_1.type)
async def catch_type(call: types.CallbackQuery, state: FSMContext):
    infrastr_type = list(call.data.split(":"))[1]
    await state.update_data(data={
        "it.name": infrastr_type
    })
    await call.message.answer(f'Ви вибрали {infrastr_type}?',
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Так", callback_data="true"),
                                      InlineKeyboardButton(text="Ні", callback_data="false")
                                  ]
                              ]))
    await Task_1.submit.set()


@dp.callback_query_handler(criteria.filter(name_of_criteria="number_of_seats"), state=Task_1.task_1)
async def choose_number_of_seats(call: types.CallbackQuery):
    await call.message.answer("Введіть <b>мінімальну-максимальну</b> кількість місць", parse_mode='html')
    await Task_1.number_of_seats.set()


@dp.message_handler(state=Task_1.number_of_seats)
async def catch_type(message: types.Message, state: FSMContext):
    min_max_number_of_seats = message.text
    await state.update_data(data={
        "min_max_number_of_seats": min_max_number_of_seats
    })
    await message.answer(f'Ви вибрали проміжок {min_max_number_of_seats}?',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [
                                 InlineKeyboardButton(text="Так", callback_data="true"),
                                 InlineKeyboardButton(text="Ні", callback_data="false")
                             ]
                         ]))
    await Task_1.submit.set()


@dp.callback_query_handler(criteria.filter(name_of_criteria="free"), state=Task_1.task_1)
async def choose_free(call: types.CallbackQuery):
    await call.message.answer("Безкоштовно?",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Так", callback_data="true"),
                                      InlineKeyboardButton(text="Ні", callback_data=" ")
                                  ]
                              ]))
    await Task_1.free.set()


@dp.callback_query_handler(state=Task_1.free)
async def catch_fre(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({
        "free": bool(call.data)
    })
    await call.message.answer(f'Ви вибрали {call.data}?',
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Так", callback_data="true"),
                                      InlineKeyboardButton(text="Ні", callback_data="false")
                                  ]
                              ]))
    await Task_1.submit.set()


@dp.callback_query_handler(criteria.filter(name_of_criteria="open_air"), state=Task_1.task_1)
async def choose_free(call: types.CallbackQuery):
    await call.message.answer("Під відкритим небом?",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Так", callback_data="true"),
                                      InlineKeyboardButton(text="Ні", callback_data=" ")
                                  ]
                              ]))
    await Task_1.open_air.set()


@dp.callback_query_handler(state=Task_1.open_air)
async def catch_fre(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({
        "open_air": bool(call.data)
    })
    await call.message.answer(f'Ви вибрали {call.data}?',
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Так", callback_data="true"),
                                      InlineKeyboardButton(text="Ні", callback_data="false")
                                  ]
                              ]))
    await Task_1.submit.set()


@dp.callback_query_handler(state=Task_1.submit)
async def submit(call: types.CallbackQuery, state: FSMContext):
    criterias = await state.get_data()
    await call.message.answer(f"Ви вибрали такі критерЇ:"
                              f"{criterias}", reply_markup=choose_criteria_ikeyboard)
    await Task_1.task_1.set()


@dp.callback_query_handler(criteria.filter(name_of_criteria="search"), state=Task_1.task_1)
async def get_result(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = await db.task1(**data)
    await call.message.answer("<b>Результат:</b>", parse_mode='html')
    if result:
        for record in result:
            record_data = dict(record)
            await call.message.answer(f"<code>Назва: {record_data.get('name')}</code>\n"
                                      f"<code>Кількість місць: {record_data.get('number_of_seats')}</code>\n"
                                      f"<code>Адреса: {record_data.get('address')}</code>\n", parse_mode='html')
        await call.message.answer("<b>Завдання №1 виконано</b>", parse_mode='html')
    else:
        await call.message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await call.message.answer("<b>Завдання №1 виконано</b>", parse_mode='html')

    await state.reset_state()

# @dp.callback_query_handler(criteria.filter(name_of_criteria="number_of_seats"))
# @dp.callback_query_handler(criteria.filter(name_of_criteria="free"))
# @dp.callback_query_handler(criteria.filter(name_of_criteria="open_air"))
