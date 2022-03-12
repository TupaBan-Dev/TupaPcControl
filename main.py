from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types

from time import time
import configparser
import webbrowser
import asyncio
import os
import keyboard
import sys
import pyautogui
import random
from PIL import Image
import platform
import psutil
import GPUtil
import humanize
from datetime import datetime
import logging

from keyboards import main_menu_1, main_menu_2, main_menu_3

# Логирование
file = open("log.txt", "w")
file.close()

logging.basicConfig(filename="log.txt", level=logging.INFO)

# Переменные

# Заблокирована ли клавиатура при старте
is_keyboard_blocked = False

# Время запуска
start_time = time()

# Обозначения конфига
config = configparser.ConfigParser()
config.read("config.ini")

# Чтение конфига
bot_token = config["My PC"]["bot_token"]
bot_password = config["My PC"]["bot_password"]
admin_id = int(config["My PC"]["admin_id"])
start_message = config["My PC"]["start_message"]
startup_message = config["My PC"]["startup_message"]
shutdown_message = config["My PC"]["shutdown_message"]

# Бот
storage = MemoryStorage()

bot = Bot(token=bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


# Классы


# Класс получения ссылки
class FSMGetLink(StatesGroup):
    link = State()


# Класс получения фотографии
class FSMGetPhoto(StatesGroup):
    photo = State()


# Клас получения сообщения
class FSMGetMessageAlert(StatesGroup):
    message_text = State()


class FSMGetMessageInput(StatesGroup):
    message_text = State()


class FSMGetMessageKeySend(StatesGroup):
    message_text = State()


# Функции


# Конвертация байтов в мегабайты
async def convert_bytes(number):
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if number < 1024.0:
            return f"{round(number, 2)} {x}"
        number /= 1024.0


# Генерация случайного имени
async def generate_random(length):
    chars = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    random_name = ""
    for i in range(length):
        random_name += random.choice(chars)
    return random_name


# Блокировка или Разблокировка клавиатуры
async def set_is_keyboard_blocked(value):
    global is_keyboard_blocked
    is_keyboard_blocked = value


# Получение видеокарт
async def get_gpu():
    for gpu in GPUtil.getGPUs():
        return gpu


# Получения аптайма
async def get_up_time():
    humanize.i18n.activate("ru_RU")
    up_time = humanize.precisedelta(
        datetime.fromtimestamp(
            psutil.boot_time()
        )
    )
    return up_time


# Старт бота
async def on_startup(_):
    info = await bot.get_me()
    print(f"""Бот запущен
    \rАйди - {info.id}
    \rСсылка - https://t.me/{info.username}""")
    if startup_message == "on":
        await bot.send_message(admin_id, "Бот запущен!")
    else:
        pass


# Выключение бота
async def on_shutdown(_):
    print("Бот выключен")
    if shutdown_message == "on":
        await bot.send_message(admin_id, "Бот выключен!")
    else:
        pass


# Команды бота

# Команда Старт
@dp.message_handler(commands="start")
async def start(message: types.Message):
    if start_message == "on":
        await message.delete()
        await message.answer("Привет, я бот для управления ПК. Введи пароль с помощью команды /password")
    else:
        pass


# Команда ввода пароля
@dp.message_handler(commands=["password", "pas", "p"])
async def password(message: types.Message):
    entered_password = message.get_args().split(" ")[0]
    if entered_password == bot_password:
        await message.delete()
        await message.answer("Меню Управления", reply_markup=main_menu_1)
    else:
        bot_message = await message.answer("Пароль введён неверно ): Попробуйте снова")
        await message.delete()
        await asyncio.sleep(5)
        await bot_message.delete()


# Команда выключения ПК
@dp.message_handler(commands=["off_pc", "turn_off_pc"])
async def command_turn_off_pc(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        bot_message = await message.answer("ПК Успешно Выключен")
        await asyncio.sleep(2)
        await bot_message.delete()
        os.system("shutdown /s /t 1")
    else:
        pass


# Команда сворачивания всех окон
@dp.message_handler(commands=["minimize_all_window", "minimize_all"])
async def command_minimize_all_windows(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        keyboard.send("Windows+d")
        bot_message = await message.answer("Все окна свёрнуты")
        await asyncio.sleep(2)
        await bot_message.delete()
    else:
        pass


# Команда открытие диспетчера задач
@dp.message_handler(commands=["open_task_manager", "task_manager"])
async def command_open_task_manager(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        keyboard.send("Ctrl+Shift+Esc")
        bot_message = await message.answer("Диспетчер задач открыт")
        await asyncio.sleep(2)
        await bot_message.delete()
    else:
        pass


# Команда нажатие пробела
@dp.message_handler(commands=["press_space", "space"])
async def command_press_space(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        keyboard.send("Space")
        bot_message = await message.answer("Пробел нажат")
        await asyncio.sleep(2)
        await bot_message.delete()
    else:
        pass


# Команда выключение бота
@dp.message_handler(commands="turn_off_bot")
async def command_turn_off_bot(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        bot_message = await message.answer("Бот выключен")
        await asyncio.sleep(2)
        await bot_message.delete()
        sys.exit()
    else:
        pass


# Команда открытие ссылки
@dp.message_handler(commands=["open_link", "link"])
async def command_open_link(message: types.Message):
    if message.from_user.id == admin_id:
        link = message.get_args().split(" ")[0]
        webbrowser.get().open_new_tab(link)
        await message.delete()
    else:
        pass


# Команда проверка статуса
@dp.message_handler(commands=["pc_status", "status"])
async def commands_bot_status(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        gpu = await get_gpu()
        bot_message = await bot.send_message(message.chat.id, f"""<code>Статус
├─Операционная система {platform.system()} {platform.architecture()[0]}
├─Оперативная Память
│ ├─Использовано {await convert_bytes(psutil.virtual_memory().used)}
│ └─Всего {await convert_bytes(psutil.virtual_memory().total)}
├─Процессор {psutil.cpu_percent()}%
├─Видеокарта
│ ├─Нагрузка {gpu.load} %
│ └─Память
│	 ├─Использовано {gpu.memoryUsed} Mb
│	 └─Всего {gpu.memoryTotal} Mb
└─Работает уже {await get_up_time()}</code>
""")
        await asyncio.sleep(10)
        await bot_message.delete()
    else:
        pass


# Команда скриншот
@dp.message_handler(commands=["screen", "screenshot"])
async def command_screenshot(message: types.Message):
    if message.from_user.id == admin_id:
        random_name = await generate_random(10)
        await message.delete()
        pyautogui.screenshot(f"screenshots/{random_name}.png")
        with open(f"screenshots/{random_name}.png", "rb") as image:
            bot_message = await message.answer_photo(image)
        os.remove(f"screenshots/{random_name}.png")
        await asyncio.sleep(10)
        await bot_message.delete()
    else:
        pass


# Команда закрыть все окна
@dp.message_handler(commands=["close_all", "close_all_window"])
async def command_close_all_window(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Надо сделать")
    else:
        pass


# Команда закрыть текущее окно
@dp.message_handler(commands="close_window")
async def command_close_window(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        keyboard.send("Alt+F4")
        bot_message = await message.answer("Текущее окно закрыто")
        await asyncio.sleep(2)
        await bot_message.delete()
    else:
        pass


# Команда открытия картинки
@dp.message_handler(content_types=["photo"])
async def command_open_image(message: types.Message):
    if message.from_user.id == admin_id:
        random_name = await generate_random(10)
        if message.caption == "/open_image":
            await message.delete()
            await message.photo[-1].download(destination_file=f"download/{random_name}.png")
            image = Image.open(f"download/{random_name}.png")
            image.show()
            os.remove(f"download/{random_name}.png")
            bot_message = await message.answer("Картинка открыта")
            await asyncio.sleep(2)
            await bot_message.delete()
        else:
            await message.delete()
    else:
        pass


# Команда блокировки клавиатуры
@dp.message_handler(commands="block_keyboard")
async def command_block_keyboard(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        if is_keyboard_blocked is False:
            for i in range(150):
                keyboard.block_key(i)
            await set_is_keyboard_blocked(True)
            bot_message = await message.answer("Клавиатура заблокирована")
            await asyncio.sleep(2)
            await bot_message.delete()
        else:
            bot_message = await message.answer("Клавиатура уже заблокирована")
            await asyncio.sleep(2)
            await bot_message.delete()
    else:
        pass


# Команда разблокировки клавиатуры
@dp.message_handler(commands="unblock_keyboard")
async def command_unblock_keyboard(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        if is_keyboard_blocked is True:
            for i in range(150):
                keyboard.unblock_key(i)
            await set_is_keyboard_blocked(False)
            bot_message = await message.answer("Клавиатура разблокирована")
            await asyncio.sleep(2)
            await bot_message.delete()
        else:
            bot_message = await message.answer("Клавиатура уже разблокирована")
            await asyncio.sleep(2)
            await bot_message.delete()
    else:
        pass


# Команда отправки сообщения на ПК
@dp.message_handler(commands="alert")
async def command_send_message_pc(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        text = message.get_args()
        bot_message = await message.answer("Сообщение отправлено")
        pyautogui.alert(text, "TupaPcControl")
        bot_message = await bot_message.edit_text("Диалоговое окно закрыто")
        await asyncio.sleep(2)
        await bot_message.delete()
    else:
        pass


# Команда отправки сообщения на ПК и получения ответа
@dp.message_handler(commands=["message_input", "input"])
async def command_send_message_input(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        text = message.get_args()
        bot_message = await message.answer("Сообщение отправлено")
        answer = pyautogui.prompt(text, "TupaPcControl")
        bot_message = await bot_message.edit_text(f"Ответ - {answer}")
        await asyncio.sleep(3)
        await bot_message.delete()
    else:
        pass


# Нажатие клавиши на клавиатуре
@dp.message_handler(commands=["key_send"])
async def command_key_send(message: types.Message):
    if message.from_user.id == admin_id:
        await message.delete()
        try:
            keyboard.send(message.get_args())
            bot_message = await message.answer(f"Клавиша <code>{message.get_args()}</code> нажата")
            await asyncio.sleep(5)
            await bot_message.delete()
        except ValueError:
            bot_message = await message.answer(f"Клавиши <code>{message.get_args()}</code> не существует")
            await asyncio.sleep(5)
            await bot_message.delete()
    else:
        pass


# Инлайн

# Инлайн выключение пк
@dp.callback_query_handler(text="turn_off_pc")
async def inline_turn_off_pc(callback: types.CallbackQuery):
    await callback.answer("ПК успешно выключен")
    os.system("shutdown /s /t 1")


# Инлайн сворачивания всех окон
@dp.callback_query_handler(text="minimize_all_windows")
async def inline_minimize_all_windows(callback: types.CallbackQuery):
    keyboard.send("Windows+d")
    await callback.answer("Все окна свёрнуты")


# Инлайн открытие диспетчера задач
@dp.callback_query_handler(text="open_task_bar")
async def inline_open_task_bar(callback: types.CallbackQuery):
    keyboard.send("Ctrl+Shift+Esc")
    await callback.answer("Диспетчер задач открыт")


# Инлайн нажатие пробела
@dp.callback_query_handler(text="turn_space")
async def inline_turn_space(callback: types.CallbackQuery):
    keyboard.send("Space")
    await callback.answer("Пробел нажат")


# Инлайн выключение бота
@dp.callback_query_handler(text="turn_off_bot")
async def inline_turn_off_bot(callback: types.CallbackQuery):
    await callback.answer("Бот выключен")
    sys.exit()


# Инлайн открытие ссылки
@dp.callback_query_handler(text="open_link")
async def inline_open_link(callback: types.CallbackQuery):
    await FSMGetLink.link.set()
    await callback.answer("Введите ссылку")


# Инлайн открытие ссылки - получение ссылки
@dp.message_handler(state=FSMGetLink.link)
async def inline_getting_link_to_open(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text
        link = data["link"]
    await message.delete()
    webbrowser.get().open_new_tab(link)
    await state.finish()
    bot_message = await message.answer(f"Ссылка {link} открыта")
    await asyncio.sleep(2)
    await bot_message.delete()


# Инлайн проверка статуса
@dp.callback_query_handler(text="check_state")
async def inline_check_state(callback: types.CallbackQuery):
    await callback.answer("Статус ПК")
    gpu = await get_gpu()
    bot_message = await bot.send_message(callback.message.chat.id, f"""<code>Статус
├─Операционная система {platform.system()} {platform.architecture()[0]}
├─Оперативная Память
│ ├─Использовано {await convert_bytes(psutil.virtual_memory().used)}
│ └─Всего {await convert_bytes(psutil.virtual_memory().total)}
├─Процессор {psutil.cpu_percent()}%
├─Видеокарта
│ ├─Нагрузка {gpu.load} %
│ └─Память
│	 ├─Использовано {gpu.memoryUsed} Mb
│	 └─Всего {gpu.memoryTotal} Mb
└─Работает уже {await get_up_time()}</code>
""")
    await asyncio.sleep(10)
    await bot_message.delete()


# Инлайн скриншот
@dp.callback_query_handler(text="screenshot")
async def inline_screenshot(callback: types.CallbackQuery):
    random_name = await generate_random(10)
    pyautogui.screenshot(f"screenshots/{random_name}.png")
    await callback.answer("Скриншот сделан")
    with open(f"screenshots/{random_name}.png", "rb") as image:
        bot_message = await bot.send_photo(callback.message.chat.id, image)
    os.remove(f"screenshots/{random_name}.png")
    await asyncio.sleep(10)
    await bot_message.delete()


# Инлайн закрытие всех окон
@dp.callback_query_handler(text="close_all_window")
async def inline_close_all_window(callback: types.CallbackQuery):
    await callback.answer("Надо сделать")


# Инлайн закрытие текущего окна
@dp.callback_query_handler(text="close_window")
async def inline_close_window(callback: types.CallbackQuery):
    keyboard.send("Alt+F4")
    await callback.answer("Текущее окно закрыто")


# Инлайн открыть картинку
@dp.callback_query_handler(text="open_image")
async def inline_open_image(callback: types.CallbackQuery):
    await FSMGetPhoto.photo.set()
    await callback.answer("Отправьте фотографию")


# Инлайн открыть картинку - получение картинку
@dp.message_handler(content_types=["photo"], state=FSMGetPhoto.photo)
async def inline_getting_link_to_open(message: types.Message, state: FSMContext):
    random_name = await generate_random(10)
    await message.photo[-1].download(destination_file=f"download/{random_name}.png")
    await message.delete()
    image = Image.open(f"download/{random_name}.png")
    image.show()
    os.remove(f"download/{random_name}.png")
    bot_message = await message.answer("Картинка открыта")
    await state.finish()
    await asyncio.sleep(2)
    await bot_message.delete()


# Инлайн блокировка клавиатуры
@dp.callback_query_handler(text="block_keyboard")
async def inline_block_keyboard(callback: types.CallbackQuery):
    if is_keyboard_blocked is False:
        for i in range(150):
            keyboard.block_key(i)
        await set_is_keyboard_blocked(True)
        await callback.answer("Клавиатура заблокирована")
    else:
        await callback.answer("Клавиатура уже заблокирована")


# Инлайн разблокировка клавиатуры
@dp.callback_query_handler(text="unblock_keyboard")
async def inline_unblock_keyboard(callback: types.CallbackQuery):
    if is_keyboard_blocked is True:
        for i in range(150):
            keyboard.unblock_key(i)
        await set_is_keyboard_blocked(False)
        await callback.answer("Клавиатура разблокирована")
    else:
        await callback.answer("Клавиатура уже разблокирована")


# Инлайн отправка уведомления
@dp.callback_query_handler(text="send_alert")
async def inline_send_alert(callback: types.CallbackQuery):
    await FSMGetMessageAlert.message_text.set()
    await callback.answer("Введите сообщение для отправки")


# Инлайн отправка уведомления - получения текста
@dp.message_handler(state=FSMGetMessageAlert.message_text)
async def inline_send_alert_get_message(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await message.delete()
        await state.finish()
        bot_message = await message.answer("Сообщение не отправлено. Вы отменили отправление")
        await asyncio.sleep(5)
        await bot_message.delete()
    else:
        bot_message = await message.answer("Сообщение отправлено")
        pyautogui.alert(message.text, "TupaPcControl")
        await message.delete()
        await state.finish()
        bot_message = await bot_message.edit_text("Диалоговое окно закрыто")
        await asyncio.sleep(5)
        await bot_message.delete()


# Инлайн отправка сообщение и получение ответа
@dp.callback_query_handler(text="send_input")
async def inline_send_alert(callback: types.CallbackQuery):
    await FSMGetMessageInput.message_text.set()
    await callback.answer("Введите сообщение для отправки")


# Инлайн отправка сообщение и получение ответа - получения текста
@dp.message_handler(state=FSMGetMessageInput.message_text)
async def inline_send_alert_get_message(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await message.delete()
        await state.finish()
        bot_message = await message.answer("Сообщение не отправлено. Вы отменили отправление")
        await asyncio.sleep(5)
        await bot_message.delete()
    else:
        bot_message = await message.answer("Сообщение отправлено")
        answer = pyautogui.prompt(message.text, "TupaPcControl")
        await message.delete()
        await state.finish()
        bot_message = await bot_message.edit_text(f"Ответ - {answer}")
        await asyncio.sleep(3)
        await bot_message.delete()


# Инлайн нажатие клавиши на клавиатуре
@dp.callback_query_handler(text="send_key")
async def inline_send_key(callback: types.CallbackQuery):
    await FSMGetMessageKeySend.message_text.set()
    await callback.answer("Введите сообщение для отправки")


# Инлайн нажатие клавиши на клавиатуре - получение текста
@dp.message_handler(state=FSMGetMessageKeySend.message_text)
async def inline_send_key_get_message(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    if message.text == "/cancel":
        await state.finish()
        bot_message = await message.answer("Клавиша не нажата. Вы отменили нажатие")
        await asyncio.sleep(5)
        await bot_message.delete()
    else:
        try:
            keyboard.send(message.text)
            bot_message = await message.answer(f"Клавиша <code>{message.text}</code> нажата")
            await asyncio.sleep(5)
            await bot_message.delete()
        except ValueError:
            bot_message = await message.answer(f"Клавиши <code>{message.text}</code> не существует")
            await asyncio.sleep(5)
            await bot_message.delete()


# Инлайн переход по страницам меню
@dp.callback_query_handler(text_contains="menu_")
async def inline_navigation_menu(callback: types.CallbackQuery):
    if callback.data.split("_")[1] == "next":
        if callback.data.split("_")[2] == "1":
            await callback.answer("Следующая страница")
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                reply_markup=main_menu_2
                                                )
        elif callback.data.split("_")[2] == "2":
            await callback.answer("Следующая страница")
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                reply_markup=main_menu_3
                                                )
        else:
            await callback.answer("Страница не найдена ):")
    elif callback.data.split("_")[1] == "back":
        if callback.data.split("_")[2] == "1":
            await callback.answer("Предыдущая страница")
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                reply_markup=main_menu_1
                                                )
        elif callback.data.split("_")[2] == "2":
            await callback.answer("Предыдущая страница")
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                reply_markup=main_menu_2
                                                )
        else:
            await callback.answer("Страница не найдена ):")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
