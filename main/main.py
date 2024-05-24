from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from Db_Kb import keyboards as kb
from Db_Kb import database as db
from dotenv import load_dotenv
import os

storage = MemoryStorage() #хранилище памяти для состояний FSM
load_dotenv()#загрузка переменных среды из .env файлa
bot = Bot(os.getenv('TOKEN')) #объект бота, использующий токен из переменной окружения
dp = Dispatcher(bot=bot, storage=storage) #диспетчер для обработки входящих сообщений и действий


async def on_startup(_): #асинхронная функция начальной загрузки бота
    await db.db_start()
    print('Бот успешно запущен!')


class NewOrder(StatesGroup):#класс состояний FSM для нового заказа
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(commands=['start'])# обработчик команды /start, инициализация данных пользователя
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAEFm3JmTf_mOcFlZ5hgnPDupYScR9jl9QACvQ8AAsj32UmL-MsRYjbQWDUE')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин Itcube!',
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор!', reply_markup=kb.main_admin)


@dp.message_handler(commands=['id'])#обработчик команды /id, отображение ID пользователя
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Каталог') #обработчик текста "Каталог", показывает категории товаров
async def catalog(message: types.Message):
    await message.answer('Выберите категорию', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')#обработчик текста "Корзина", выводит сообщение о пустой корзине
async def cart(message: types.Message):
    await message.answer('Корзина пуста!')


@dp.message_handler(text='Контакты')#oбработчик текста "Контакты", показывает контактную информацию
async def contacts(message: types.Message):
    await message.answer('Покупать товар у них: @Obama249, @kokosik334')


@dp.message_handler(text='Админ-панель')#обработчик текста "Админ-панель", показывает админские возможности
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Добавить товар')#обработчик текста "Добавить товар", добавление товара (для администратора)
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer('Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')

@dp.message_handler(text='Удалить товар')#обработчик текста "Удалить товар", удаление товара (для администратора)
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer('Товар удалён')


@dp.callback_query_handler(state=NewOrder.type) #обработчик типа товара (callback_query) и установка следующего состояния
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name) #обработчик названия товара и переход к следующему состоянию
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc) #обработчик описания товара и переход к следующему состоянию
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price) # обработчик цены товара и переход к следующему состоянию
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)#обработчик проверки наличия фотографии товара, вывод предупреждения
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)#Этот обработчик реагирует на сообщения-фотографии, когда пользователь находится в состоянии ожидания
#фотографии товара для заказа (определено состоянием NewOrder.photo).

async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler() #Этот обработчик реагирует на все текстовые сообщения, для которых не существует других обработчиков.
 #  - Отправляет ответное сообщение "Я тебя не понимаю.".
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler()# Этот обработчик реагирует на inline клавиатурные callback-запросы.
  # - Проверяет значение callback_query.data:
 #    - Если равно 'pc', отправляет сообщение "Вы выбрали компьютер".
  #   - Если равно 'nout', отправляет сообщение "Вы выбрали ноутбук".
  #   - Если равно 'mon', отправляет сообщение "Вы выбрали моноблок".

async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'pc':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали компьютер')
    elif callback_query.data == 'nout':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали ноутбук')
    elif callback_query.data == 'mon':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали моноблок')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)# Запуск цикла обновлений бота executor.start_polling() для опроса сервера Telegram.
    # Вызывает on_startup для инициализации при запуске. skip_updates=True пропускает обработку накопленных обновлений.