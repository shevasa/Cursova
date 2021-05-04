from aiogram.dispatcher.filters.state import StatesGroup, State


class Task_1(StatesGroup):
    task_1 = State()
    type = State()
    number_of_seats = State()
    free = State()
    open_air = State()
    submit = State()