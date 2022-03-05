from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_1 = InlineKeyboardMarkup(row_width=2)
main_menu_button_1 = InlineKeyboardButton(text="❌ Выключить ПК", callback_data="turn_off_pc")
main_menu_button_2 = InlineKeyboardButton(text="📥 Свернуть все окна", callback_data="minimize_all_windows")
main_menu_button_3 = InlineKeyboardButton(text="🖥 Диспетчер задач", callback_data="open_task_bar")
main_menu_button_4 = InlineKeyboardButton(text="🌌 Нажать пробел", callback_data="turn_space")
main_menu_button_5 = InlineKeyboardButton(text="➖ Выключить Бота", callback_data="turn_off_bot")
main_menu_button_6 = InlineKeyboardButton(text="🔗 Открыть ссылку", callback_data="open_link")
main_menu_button_7 = InlineKeyboardButton(text="🤖 Статус", callback_data="check_state")
main_menu_button_8 = InlineKeyboardButton(text="▶", callback_data="menu_next_1")
main_menu_1.add(main_menu_button_1, main_menu_button_2,
                main_menu_button_3, main_menu_button_4,
                main_menu_button_5, main_menu_button_6,
                main_menu_button_7, main_menu_button_8)

main_menu_2 = InlineKeyboardMarkup(row_width=2)
main_menu_button_1 = InlineKeyboardButton(text="📸 Скриншот", callback_data="screenshot")
main_menu_button_2 = InlineKeyboardButton(text="🪟 Закрыть все окна", callback_data="close_all_window")
main_menu_button_3 = InlineKeyboardButton(text="❎ Закрыть текущее окно", callback_data="close_window")
main_menu_button_4 = InlineKeyboardButton(text="🖼 Открыть картинку", callback_data="open_image")
main_menu_button_5 = InlineKeyboardButton(text="🔒 Заблокировать Клавиатуру", callback_data="block_keyboard")
main_menu_button_6 = InlineKeyboardButton(text="🔓 Разблокировать Клавиатуру", callback_data="unblock_keyboard")
main_menu_button_7 = InlineKeyboardButton(text="◀️", callback_data="menu_back_1")
main_menu_button_8 = InlineKeyboardButton(text="▶", callback_data="menu_next_2")
main_menu_2.add(main_menu_button_1, main_menu_button_2,
                main_menu_button_3, main_menu_button_4,
                main_menu_button_5, main_menu_button_6,
                main_menu_button_7, main_menu_button_8)

main_menu_3 = InlineKeyboardMarkup(row_width=2)
main_menu_button_1 = InlineKeyboardButton(text="❗ Отправить уведомление", callback_data="send_alert")
main_menu_button_2 = InlineKeyboardButton(text="❓ Отправить сообщение", callback_data="send_input")
main_menu_button_3 = InlineKeyboardButton(text="⌨ Нажать клавишу", callback_data="send_key")
main_menu_button_4 = InlineKeyboardButton(text="◀️", callback_data="menu_back_2")
main_menu_button_5 = InlineKeyboardButton(text="▶", callback_data="menu_next_3")
main_menu_3.add(main_menu_button_1, main_menu_button_2,
                main_menu_button_3,
                main_menu_button_4, main_menu_button_5)
