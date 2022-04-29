from config import tg_bot_token_Airat, admins, tg_bot_token_Nail
import markups as nav
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import change_xlsx
import datetime
from readd_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import MediaGroup
from aiogram.types.input_file import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=tg_bot_token_Airat)
dp = Dispatcher(bot, storage=storage)


class SendMessage(StatesGroup):
    id_person = State()
    message_from_person = State()


class BagReport(StatesGroup):
    bag_message = State()


class AddPhoto(StatesGroup):
    ph = State()


@dp.message_handler(state="*", commands='назад')
async def support_team(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await bot.send_message(message.from_user.id, "Вы вернулись в главное меню", reply_markup=nav.minorMenu)
    if not current_state:
        return
    await state.finish()


@dp.message_handler(commands=["сообщить_о_баге"])
async def report_for_bag(message: types.Message):
    await BagReport.bag_message.set()
    await bot.send_message(message.from_user.id, f"Пожалуйста, подробно опишите возникшую проблему"
                                                 f" в ОДНОМ сообщеении. Админы ответят в течении суток.")


@dp.message_handler(state=BagReport.bag_message)
async def info_from_school(message: types.Message, state: FSMContext):
    add_support_msg(message.text, message.from_user.id)
    await state.finish()


class AddSchool(StatesGroup):
    msg = State()


@dp.message_handler(commands=["добавить_школу"])
async def add_school(message: types.Message):
    await AddSchool.msg.set()
    media = MediaGroup()
    media.attach_photo(InputFile('files/images/1.png'))
    media.attach_photo(InputFile('files/images/2.png'))
    media.attach_photo(InputFile('files/images/3.png'))
    await bot.send_media_group(message.from_user.id, media=media)


@dp.message_handler(state=AddSchool.msg)
async def info_from_school(message: types.Message, state: FSMContext):
    for admin_id in admins:
        await bot.send_message(admin_id, f"{message.from_user.id}\nПопытка добавить школу\n{message.text}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите район и школу, и я отправлю вам школьное меню на сегодня.",
                           reply_markup=nav.inlineMenu)


@dp.message_handler(commands=["support"])
async def support_team(message: types.Message):
    if message.from_user.id not in admins:
        await bot.send_message(message.from_user.id, f"Вы можете предложить школу либо сообщить о баге",
                               reply_markup=nav.reportMenu)
        # add_support_msg(message.text, message.from_user.id)  # не здесь а в этой тупой машине состояний
        # СДЕЛАТЬ ПОМОЩЬ
    else:
        await bot.send_message(message.from_user.id, f"Панель администратора", reply_markup=nav.adminPanelMenu)


@dp.message_handler(commands=["получить_сообщение"])
async def support_team(message: types.Message):
    await bot.send_message(message.from_user.id, f'{get_support_msg()}')


@dp.message_handler(commands=["написать_кому-то"])
async def support_team(message: types.Message):
    if message.from_user.id not in admins:
        return
    await SendMessage.id_person.set()
    await bot.send_message(message.from_user.id, "Кому ты хочешь написать?(id)")


@dp.message_handler(state=SendMessage.id_person)
async def get_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await message.reply('Что ты хочешь написать?')
    await SendMessage.next()


@dp.message_handler(state=SendMessage.message_from_person)
async def snd_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data['id'])
        await bot.send_message(data['id'], message.text)
    await message.reply('Сообщение отпралено, надеюсь, id был верным )))')
    await state.finish()


@dp.message_handler(commands=["добавить_фото"])
async def support_team(message: types.Message):
    if message.from_user.id not in admins:
        return
    await bot.send_message(message.from_user.id, "Отправьте фото")
    await AddPhoto.ph.set()


@dp.message_handler(content_types=["photo"], state=AddPhoto.ph)
async def load_photo(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Фото сохранено")
    await message.photo[-1].download()
    await state.finish()


@dp.message_handler()
async def get_menu(message: types.Message):
    try:
        if message.text == 'Получить меню' and check_users(message.from_user.id):
            sch_full_name, data_update, menu, link = read_db(get_school(message.from_user.id), 'n_chelny')
            if str(datetime.date.today()) == data_update:
                await bot.send_message(message.from_user.id, menu)
            else:
                try:
                    await bot.send_message(message.from_user.id, "Пожалуйста, подождите")
                    change_xlsx.give_menu(link + str(datetime.date.today()).strip() + '-sm.xlsx')
                    write_menu_date_update(sch_full_name, change_xlsx.print_menu('menu.xlsx'), datetime.date.today())
                    sch_full_name, data_update, menu, link = read_db(get_school(message.from_user.id), 'n_chelny')
                    await bot.send_message(message.from_user.id, menu)
                except:
                    await bot.send_message(message.from_user.id, "Вашего меню ещё нет...")
        elif message.text == 'Получить меню':
            await bot.send_message(message.from_user.id, "Пожалуйста, выберите школу", reply_markup=nav.inlineMenu)
        elif message.text == 'Изменить школу':
            clear_db_users(message.from_user.id)
            await bot.send_message(message.from_user.id, "Вы перешли в главное меню", reply_markup=nav.inlineMenu)
        else:
            await bot.send_message(message.from_user.id, "Я вас не понимаю", reply_markup=nav.minorMenu)
    except:
        await message.reply(f"Произошла какая-то ошибка.")


@dp.callback_query_handler(text="btn_n_chelny")
async def n_chelny(callback: types.CallbackQuery):
    await callback.message.answer("Выберите школу", reply_markup=nav.inlineMinorMenu)


@dp.callback_query_handler(text="btn_lic_int79")
async def lic_int79(callback: types.CallbackQuery):
    if not check_users(callback.from_user.id):
        write_school(callback.from_user.id, "Лицей-интернат №79")
        await callback.message.answer("Спасибо, теперь, если ваша школа опубликовала меню на сайте"
                                      " edu.tatar, то вы можете его получить.", reply_markup=nav.minorMenu)
        await callback.answer('Вы выбрали школу')
    else:
        await callback.answer('Вы уже выбрали школу')


@dp.callback_query_handler(text="btn_sch78")
async def sch78(callback: types.CallbackQuery):
    if not check_users(callback.from_user.id):
        write_school(callback.from_user.id, "Лицей №78")
        await callback.message.answer("Спасибо, теперь, если ваша школа опубликовала меню на сайте"
                                      " edu.tatar, то вы можете его получить.", reply_markup=nav.minorMenu)
        await callback.answer('Вы выбрали школу')
    else:
        await callback.answer('Вы уже выбрали школу')


@dp.callback_query_handler(text="btn_gym26")
async def gym26(callback: types.CallbackQuery):
    if not check_users(callback.from_user.id):
        write_school(callback.from_user.id, "Гимназия №26")
        await callback.message.answer("Спасибо, теперь, если ваша школа опубликовала меню на сайте"
                                      " edu.tatar, то вы можете его получить.", reply_markup=nav.minorMenu)
        await callback.answer('Вы выбрали школу')
    else:
        await callback.answer('Вы уже выбрали школу')


if __name__ == '__main__':
    executor.start_polling(dp)
