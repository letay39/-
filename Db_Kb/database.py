import sqlite3 as sq


async def db_start():  #создает подключение к базе данных, создает таблицы accounts и items и сохраняет изменения в базе данных
    global db, cur
    db = sq.connect('tg.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "price TEXT, "
                "photo TEXT, "
                "brand TEXT)")
    db.commit()


async def cmd_start_db(user_id):  # выполняет команду SELECT, выбирая пользователя с заданным tg_id, если пользователь не найден, добавляет его в базу данных
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


async def add_item(state): #добавляет запись в таблицу items, используя данные из data, обновляет изменения в базе данных
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['photo'], data['type']))
    db.commit()