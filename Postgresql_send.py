import psycopg2
from parser_site import Parser


class PostgreSql:
    def __init__(self):
        """Подключение к базе данных"""
        self.db = psycopg2.connect(
            host='localhost',
            database='parser_bot_db',
            user='postgres',
            password='123456'
        )
        self.cursor = self.db.cursor()

    def create_table(self, name_table):
        """Создание таблицы"""
        self.cursor.execute(f'''
            DROP TABLE IF EXISTS {name_table};
            CREATE TABLE IF NOT EXISTS {name_table} (
                id SERIAL NOT NULL PRIMARY KEY,
                title VARCHAR(255),
                text TEXT,
                date VARCHAR(30),
                week_day VARCHAR(30),
                place TEXT,
                url TEXT
            )
        ''')

    def insert_data(self, **kwargs):
        """Добавление данных в базу данных"""
        self.cursor.execute('''INSERT INTO znaniya (title, text, date, week_day, place, url) 
            VALUES (%s, %s, %s, %s, %s, %s)''',
                            (kwargs['title'], kwargs['text'], kwargs['date'],
                             kwargs['week_day'], kwargs['place'],
                             kwargs['url']))


# Создание базы данных
db = PostgreSql()
# Создание таблицы
db.create_table('znaniya')
# Парсинг
znaniya = Parser(url='https://www.afisha.uz/znaniya/')
content = znaniya.run()

# Добавелние данных в базу
for item in content:
    db.insert_data(
        title=item['title'], text=item['content'], date=item['date'],
        week_day=item['week_day'], place=item['place'], url=item['url']
    )

# Вывести всё в консоль
db.cursor.execute('''SELECT * FROM znaniya''')
data = db.cursor.fetchall()
for item in data:
    print(item)
