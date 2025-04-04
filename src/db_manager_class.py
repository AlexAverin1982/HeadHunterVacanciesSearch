import copy

import psycopg2
from copy import deepcopy

"""
Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests
.
Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку 
psycopg2
.
Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
"""


def fill_fields_and_values(data: dict, separator: str, ignore_fields: list[str], only_fields: list[str]) -> tuple[
    str, str]:
    """
        Вспомогательная функция для подготовки списков имен полей и их значений для запросов
    """
    fields = ''
    values = ''
    for field, value in data.items():
        if field in ignore_fields:
            continue
        if len(only_fields) and not (field in only_fields):
            continue
        if value is None:
            continue
        if (field != '') and not isinstance(value, dict):
            fields += f"{field}{separator}"
            if isinstance(value, str):
                if value.find("'") > -1:
                    value = value.replace("'", "''")
                values += f"'{value[:150]}'{separator}"
            else:
                values += f"{value}{separator}"

    return fields, values


class DBManager:
    """
    Класс DBManager будет подключаться к БД PostgreSQL
    """

    def __init__(self):  # type ignore
        self.__db_name: str = ''
        self.__connection_settings: dict = {}
        self.__connection = None
        self.__error_message: str = ''
        self.pending_data: dict = {}  # данные, которые движок будет дополнительно запрашивать у приложения

    @property
    def error_message(self) -> str:
        """
        Сообщение об ошибке
        """
        return self.__error_message

    def connected(self) -> bool:
        """
            признак активности подключения к базе данных
        """
        return bool(self.__connection)

    @property
    def connection_settings(self) -> dict:
        """
        Настройки для подключения к серверу баз данных
        """
        return self.__connection_settings

    @connection_settings.setter
    def connection_settings(self, settings: dict) -> None:
        """
        установка настроек подключения к серверу
        """
        self.__connection_settings.update(settings)

    def connect(self) -> None:
        """
        подключение к существующей базе
        """

        if self.__connection:
            self.__connection.close()

        try:
            self.__connection = psycopg2.connect(dbname=self.__connection_settings.get('dbname'),
                                                 user=self.__connection_settings.get('user'),
                                                 password=self.__connection_settings.get('password'),
                                                 host=self.__connection_settings.get('host'),
                                                 port=self.__connection_settings.get('port'))
        except psycopg2.OperationalError:
            self.__error_message = 'Подключиться к базе данных не удалось'

        else:
            self.__connection.autocommit = True

    def disconnect(self) -> None:
        """
        отключение от базы
        """
        if self.__connection:
            self.__connection.close()

    def __str__(self) -> str:
        """
        :return: Настройки подлкючения к серверу и имя базы данных
        """
        result = ''
        if self.__connection:
            result += str(self.__connection.dsn)
        return result

    def base_exists(self, dbname: str) -> bool:
        result = False
        if not self.__connection:
            old_settings = copy.deepcopy(self.__connection_settings)
            self.__connection_settings['dbname'] = 'postgres'
            self.__connection_settings['user'] = 'postgres'
            self.__connection_settings['password'] = old_settings.get('rootpass')
            self.connect()

            if self.__error_message:
                self.__connection_settings = old_settings
                self.connect()
            else:
                query = f"SELECT true WHERE EXISTS (SELECT datname FROM pg_database where datname='{dbname}');"
                cur = self.__connection.cursor()
                try:
                    cur.execute(query)
                except psycopg2.OperationalError:
                    self.__error_message = 'Запрос о проверке существования базы данных выполнить не удалось'
                else:
                    result = cur.fetchone()
                self.__connection_settings = old_settings
                self.connect()
        return result

    def create_db(self) -> None:
        """
        создание базы данных с пустыми таблицами
        """
        old_settings = copy.deepcopy(self.__connection_settings)
        new_user = old_settings.get('user')
        new_base = old_settings.get('dbname')
        new_user_password = old_settings.get('password')

        self.__connection_settings['dbname'] = 'postgres'
        self.__connection_settings['user'] = 'postgres'
        self.__connection_settings['password'] = old_settings.get('rootpass')
        self.connect()

        # dbname = self.__connection_settings.get('dbname')
        # conn = psycopg2.connect("dbname=postgres user=postgres password=89109995794")
        conn = self.__connection
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        conn.autocommit = True

        if new_user != 'postgres':
            query = """
DO
$$BEGIN
IF EXISTS (SELECT FROM pg_roles WHERE rolname = '{}') THEN
    EXECUTE 'DROP OWNED BY {}';
END IF;
END$$;        
        """.format(new_user, new_user)

            try:
                cur.execute(query)
            except psycopg2.OperationalError:
                self.__error_message = 'Не получилось удалить объекты, которыми владеет удаляемый пользователь'
                return

        try:
            cur.execute(f"DROP DATABASE IF EXISTS {new_base};")
        except psycopg2.OperationalError:
            self.__error_message = f"Не получилось удалить базу данных {new_base}"
            return
        try:
            cur.execute(f"CREATE DATABASE {new_base};")
        except psycopg2.OperationalError:
            self.__error_message = f"Не получилось создать базу данных {new_base}"
            return

        if new_user != 'postgres':
            try:
                cur.execute(f"DROP USER IF EXISTS {new_user};")
            except psycopg2.OperationalError:
                self.__error_message = f"Не получилось удалить пользователя {new_user}"
                return
            try:
                query = "CREATE USER {} PASSWORD '{}';".format(new_user, new_user_password)
                cur.execute(query)
            except psycopg2.OperationalError:
                self.__error_message = f"Не получилось создать пользователя {new_user}"
                return
            try:
                cur.execute(f"ALTER DATABASE hh OWNER TO {new_user};")
            except psycopg2.OperationalError:
                self.__error_message = f"Пользователь {new_user} не стал владельцем базы данных {new_base}"
                return
        cur.close()
        conn.close()

        # conn = psycopg2.connect("dbname=hh user=hhuser password=123456")
        self.__connection_settings = deepcopy(old_settings)
        self.connect()
        conn = self.__connection
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        conn.autocommit = True
        # cur.execute("GRANT USAGE ON SCHEMA public TO hhuser;")
        # cur.execute(f"GRANT CREATE ON SCHEMA public TO hhuser;")
        # cur.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO hhuser;")
        # cur.execute("GRANT ALL PRIVILEGES ON DATABASE hh to hhuser")
        try:
            cur.execute('DROP TABLE IF EXISTS vacancy;')
        except psycopg2.OperationalError:
            self.__error_message = "Не удалось удалить таблицу vacancy"
            return

        query = ("CREATE TABLE public.vacancy ( id char(9) NOT NULL, name varchar(200) NOT NULL, " +
                 "area_id varchar(10), address varchar(150), employer_id char(8), " +
                 "salary int DEFAULT 0, currency varchar(4), requirement text, " +
                 "responsibility text, alternate_url varchar(150)," +
                 "CONSTRAINT pk_vacancy_id PRIMARY KEY ( id ));")

        try:
            cur.execute(query)
        except psycopg2.OperationalError:
            self.__error_message = "Не удалось создать таблицу vacancy"
            return

        try:
            cur.execute('DROP TABLE IF EXISTS employer;')
        except psycopg2.OperationalError:
            self.__error_message = "Не удалось удалить таблицу employer"
            return

        try:
            query = ("CREATE TABLE public.employer ( id char(8) NOT NULL, name varchar(150) NOT NULL, " +
                     "alternate_url varchar(150) NOT NULL, url varchar(150), vacancies_url varchar(150), " +
                     "vacancies_count int DEFAULT 0, area_id varchar(20)," +
                     "CONSTRAINT pk_employer_id PRIMARY KEY ( id ));")
            cur.execute(query)
        except psycopg2.OperationalError:
            self.__error_message = "Не удалось создать таблицу vacancy"
            return

        query = """ALTER TABLE public.vacancy ADD CONSTRAINT fk_vacancy_employer FOREIGN KEY ( employer_id ) 
        REFERENCES public.employer( id ) ON DELETE CASCADE ON UPDATE CASCADE;"""
        try:
            cur.execute(query)
        except psycopg2.OperationalError:
            self.__error_message = "Не удалось добавить внешний ключ fk_vacancy_employer"
            return

        cur.close()
        conn.close()

    def connection_status(self) -> str:
        if self.__connection:
            return str(self.__connection)
        else:
            return 'Подключение к серверу отсутствует'

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """
        — получает список всех компаний и количество вакансий у каждой компании.
        """
        result = []
        conn = self.__connection
        if not conn:
            return result
        cur = conn.cursor()
        conn.autocommit = True
        query = f"SELECT id, name, vacancies_count FROM employer ORDER BY vacancies_count desc, name;"
        cur.execute(query)

        for data_item in cur.fetchall():
            result.append(f"id: {data_item[0]} -- name: {data_item[1]} --- vacancies: {data_item[2]}")

        return result

    def get_all_vacancies(self) -> list:
        """
        — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        result = []
        self.connect()
        conn = self.__connection
        if not conn:
            return result
        cur = conn.cursor()
        conn.autocommit = True

        query = """select v.id, v.name, v.salary, v.currency, e.name, v.alternate_url 
from vacancy v join employer e
on v.employer_id = e.id;"""
        cur.execute(query)

        for data_item in cur.fetchall():
            result.append(f"ID вакансии: {data_item[0]}; требуется: {data_item[1]}; работодатель: {data_item[4]}; " +
                          f"зарплата: {data_item[2]} {data_item[3]}; ссылка на вакансию: {data_item[5]}")

            # result.append(f"Вакансия: {data_item[0]}; работодатель: {data_item[1]}; зарплата: " +
            #               f"{data_item[2]} {data_item[3]}; ссылка на вакансию: {data_item[4]}")

        return result

    def get_avg_salary(self) -> int:
        """
        — получает среднюю зарплату по вакансиям.
        """
        result = 0
        self.connect()
        if self.connected():
            cur = self.__connection.cursor()
            cur.execute("select AVG(salary) from vacancy where salary > 0;")
            result = round(cur.fetchone()[0], 0)
        return result

    def get_vacancies_with_higher_salary(self) -> list[str]:
        """
        — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        result = ['Список вакансий с зарплатой выше средней:']
        avg_salary = self.get_avg_salary()
        self.connect()
        conn = self.__connection
        if not conn:
            return result
        cur = conn.cursor()
        conn.autocommit = True

        query = f"""select v.id, v.name, v.salary, v.currency, e.name, v.alternate_url 
        from vacancy v join employer e
        on v.employer_id = e.id
        WHERE v.salary > {avg_salary};"""
        cur.execute(query)

        for data_item in cur.fetchall():
            result.append(f"ID вакансии: {data_item[0]}; требуется: {data_item[1]}; работодатель: {data_item[4]}; " +
                          f"зарплата: {data_item[2]} {data_item[3]}; ссылка на вакансию: {data_item[5]}")

        return result

    def get_vacancies_with_keyword(self, keywords: str, separator: str = ',') -> list:
        """
        — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        result = []
        self.connect()
        conn = self.__connection
        if not conn:
            return result
        cur = conn.cursor()
        conn.autocommit = True

        for keyword in keywords.split(separator):
            result.append('-' * 30 + f" ключевое слово: {keyword} " + '-' * 30)

            query = f"""select v.id, v.name, v.salary, v.currency, e.name, v.alternate_url 
            from vacancy v join employer e
            on v.employer_id = e.id
            WHERE v.name LIKE '%{keyword}%';"""
            cur.execute(query)

            for data_item in cur.fetchall():
                result.append(
                    f"ID вакансии: {data_item[0]}; требуется: {data_item[1]}; работодатель: {data_item[4]}; " +
                    f"зарплата: {data_item[2]} {data_item[3]}; ссылка на вакансию: {data_item[5]}")

        if len(result):
            result.insert(0, 'Список вакансий, название которых содержит указанные ключевые слова:')
        return result

    def insert_employer_data(self, employer_data: dict | list, allow_without_vacancies: bool = True) -> None:
        """
        Вставляем данные о работодателе в таблицу
        """

        def insert_item(employer_data_item) -> None:
            employer_id = employer_data_item.get('id')
            if employer_id:
                # with self.__connection.cursor() as cursor:
                query = f"SELECT name FROM employer WHERE id='{employer_id}';"
                cur.execute(query)

                tablename = 'employer'
                id = employer_data_item.get('id')
                open_vacancies = employer_data_item.get('open_vacancies')
                separator = '||'

                if not cur.rowcount:
                    if not allow_without_vacancies:
                        if not ('open_vacancies' in employer_data_item.keys()):
                            return
                        elif employer_data_item['open_vacancies'] == 0:
                            return
                    separator = ','
                    fields, values = fill_fields_and_values(employer_data_item,
                                                            separator,
                                                            ['open_vacancies'], [])
                    fields = fields[:-1]
                    values = values[:-1]

                    query = f"INSERT INTO {tablename} ({fields}) VALUES ({values});"
                    cur.execute(query)

                    if open_vacancies is not None:
                        if isinstance(open_vacancies, int):
                            if allow_without_vacancies or open_vacancies != 0:
                                query = f"UPDATE {tablename} SET vacancies_count={open_vacancies} WHERE id='{id}';"
                                cur.execute(query)
                else:
                    fields, values = fill_fields_and_values(employer_data_item,
                                                            separator,
                                                            ['id', 'open_vacancies'], [])
                    # set_part_list = []
                    fields_list = fields.split(separator)[:-1]
                    values_list = values.split(separator)[:-1]
                    # for field, value in zip(fields, values):
                    #     set_part_list.append(f"{field}={value}")
                    #     set_part_str = ','.join(set_part_list)
                    set_part_list = [f"{field}={value}" for field, value in zip(fields_list, values_list)]
                    set_part_str = ','.join(set_part_list)
                    query = f"UPDATE {tablename} SET {set_part_str} WHERE id='{id}';"
                    cur.execute(query)
                    if open_vacancies is not None:
                        if isinstance(open_vacancies, int):
                            if allow_without_vacancies or open_vacancies != 0:
                                query = f"UPDATE {tablename} SET vacancies_count={open_vacancies} WHERE id='{id}';"
                                cur.execute(query)

        # conn = psycopg2.connect("dbname=hh user=hhuser password=123456")
        # conn.set_client_encoding('UTF8')
        if not self.__connection:
            self.connect()
        if not self.__connection:
            self.__error_message = 'Не удалось подключиться к базе данных'
            return
        conn = self.__connection
        try:
            cur = conn.cursor()
        except psycopg2.InterfaceError:
            self.__error_message = "Подключение потеряно"
            return
        conn.autocommit = True

        if isinstance(employer_data, dict):
            insert_item(employer_data)
        elif isinstance(employer_data, list):
            for item in employer_data:
                insert_item(item)

    def show_employers(self) -> None:
        """
        Вставляем данные о работодателе в таблицу
        """
        conn = psycopg2.connect("dbname=hh user=hhuser password=123456")
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        conn.autocommit = True
        query = f"SELECT id, name FROM employer;"
        cur.execute(query)

        for record in cur.fetchall():
            print(record)

        """
        if not self.__connection:
            self.connect()
        if self.__connection:
            employer_id = employer_data.get('id')
            cursor = self.__connection.cursor()
            if employer_id:
                # with self.__connection.cursor() as cursor:
                sql = f'SELECT name FROM employer ' + f"WHERE id='{employer_id}';"
                self.__connection.cursor().execute(sql)

                if not cursor.rowcount:
                    fields, values = fill_fields_and_values(employer_data)
                    query = f"INSERT INTO {fields} VALUES ({values});"
                    cursor.execute(query)
                    self.__connection.commit()
        """

    def insert_vacancies_data(self, vacancies_data: dict | list) -> None:
        """
        Добавляем/обновляем в базу данных записи о вакансиях и,если надо, о работодателях
        """

        def add_vacancy(vacancy_data: dict) -> None:
            """
            Добавляем/обновляем в базу данных записи об одной вакансии и,если надо, о работодателях
            """
            if not self.__connection:
                self.connect()

            id = vacancy_data.get('id')
            emp_id = vacancy_data.get('employer', {}).get('id')
            name = vacancy_data.get('name')

            conn = self.__connection

            if not self.__connection:
                self.__error_message = ("Не удалось подключиться к базе данных " +
                                        f" {self.__connection_settings.get('dbname')}")
                return

            cur = conn.cursor()
            conn.autocommit = True
            if not id:
                self.__error_message = f"Не указан идентификатор вакансии {name}"
                return

            if not name:
                self.__error_message = f"Не указано название вакансии {id}"
                return

            if not emp_id:
                self.__error_message = f"В вакансии {id} не указан работодатель"
                return

            salary = vacancy_data.get('salary', {}).get('from', 0)
            alternate_url = vacancy_data.get('alternate_url')
            area_id = vacancy_data.get('area', {}).get('id')
            currency = vacancy_data.get('salary', {}).get('currency')
            address = vacancy_data.get('address')
            if address and isinstance(address, dict):
                address = address.get('raw', '')
            if address is None:
                address = ''
            if salary is None:
                salary = 0

            fields = 'id, name, employer_id, salary'
            values = f"'{id}', '{name}', '{emp_id}', {salary}"
            if area_id:
                fields += ',area_id'
                values += f",'{area_id}'"
            if address:
                fields += ',address'
                if address.find("'"):
                    address = address.replace("'", "''")
                values += f",'{address}'"
            if currency:
                fields += ',currency'
                values += f",'{currency}'"
            if alternate_url:
                fields += ',alternate_url'
                values += f",'{alternate_url}'"

            cur.execute(f"SELECT name from vacancy WHERE id='{id}'")
            if cur.rowcount:
                query = f"""UPDATE vacancy SET name='{name}', employer_id='{emp_id}',
                 salary={salary}, address='{address}'"""
                if area_id:
                    query += f", area_id='{area_id}'"
                if alternate_url:
                    query += f", alternate_url='{alternate_url}'"
                query += f" WHERE id='{id}';"
            else:
                # заранее считаем, что работодатели уже присутствуют в базе и здесь это не проверяется
                query = f"INSERT INTO vacancy ({fields}) VALUES ({values});"
            cur.execute(query)

        if isinstance(vacancies_data, dict):
            add_vacancy(vacancies_data)
        elif isinstance(vacancies_data, list):
            for vac_data in vacancies_data:
                self.connect()
                if self.connected():
                    add_vacancy(vac_data)
                    self.disconnect()
