from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура с кнопками "Каталог", "Корзина", "Контакты"
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True) #клавиатура с кнопками "Каталог", "Корзина", "Контакты", "Админ-панель"
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура с кнопками "Добавить товар", "Удалить товар"
admin_panel.add('Добавить товар').add('Удалить товар')

catalog_list = InlineKeyboardMarkup(row_width=2) #клавиатура с кнопками для выбора категории товаров: "Компьютеры", "Ноутбуки", "Моноблоки"
catalog_list.add(InlineKeyboardButton(text='Компьютеры', callback_data='pc'),
                 InlineKeyboardButton(text='Ноутбуки', callback_data='nout'),
                 InlineKeyboardButton(text='Моноблоки', callback_data='mon'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True) #клавиатура с кнопкой "Отмена"
cancel.add('Отмена')