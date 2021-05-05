from aiogram import types

from loader import dp, db


@dp.message_handler(text="Завдання №4")
async def task4(message: types.Message):
    artists = await db.task4()
    await message.answer("<b>Результат:</b>", parse_mode='html')
    if artists:
        for record in artists:
            record_data = dict(record)
            await message.answer(f"<code>Ім'я артиста: {record_data.get('artist_name')}</code>\n"
                                      f"<code>Жанр: {record_data.get('genre')}</code>\n",
                                      parse_mode='html')
        await message.answer("<b>Завдання №4 виконано</b>", parse_mode='html')
    else:
        await message.answer("<code>Таких записів немає!</code>", parse_mode='html')
        await message.answer("<b>Завдання №4 виконано</b>", parse_mode='html')