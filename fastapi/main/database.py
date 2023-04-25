import psycopg2
from psycopg2 import Error
from datetime import datetime




class Database:
    connection = None
    username = 'postgres'
    password = ''
    host = '127.0.0.1'
    db_name = 'postgres'
    table_name = 'records'

    def connect_to_db(self):
        try:
            self.connection = psycopg2.connect(user=self.username,
                                               password=self.password,
                                               host=self.host,
                                               database=self.db_name)
            self.connection.autocommit = True
        except Error as e:
            print(f'DB initialize error: {e.pgerror} {e.diag}')

    def insert_data(self, id, value):
        error = ''
        if not self.connection:
            error = 'DB is not connected'
            print(error)
            return (False, error)
        result = False
        try:
            cursor = self.connection.cursor()
            timestamp = int(round(datetime.now().timestamp()))
            cursor.execute(f'''INSERT INTO {self.table_name} (id, value,
                           timestamp) VALUES({id}, '{value}', {timestamp})
                           ON CONFLICT (id) DO NOTHING RETURNING id;''')
            if cursor.fetchone():
                print(f'Record {value} with "id" {id} stored in DB')
                result = True
            else:
                error = f'Record with "id" {id} is already in DB'
                print(error)
        except Error as e:
            error = f'DB error: {e.pgerror} {e.diag}'
            print(error)
        finally:
            cursor.close()
            return (result, error)

    def change_data(self, id, value):
        error = ''
        if not self.connection:
            error = 'DB is not connected'
            print(error)
            return (False, error)
        result = False
        try:
            cursor = self.connection.cursor()
            timestamp = int(round(datetime.now().timestamp()))
            cursor.execute(f'''UPDATE {self.table_name} SET value = '{value}',
                           timestamp = {timestamp} WHERE id = {id};''')
            result = cursor.rowcount == 1
            if result:
                print(f'"value" {value} with "id" {id} was changed if DB')
            else:
                error = f'"value" {value} with "id" {id} not stored in DB'
                print(error)
        except Error as e:
            error = f'DB error: {e.pgerror} {e.diag}'
            print(error)
        finally:
            cursor.close()
            return (result, error)

    def read_data(self, fields, limit=None, offset=None):
        error = ''
        if not self.connection:
            error = 'DB is not connected'
            print(error)
            return (False, error, [])
        records = []
        result = True
        where = ''
        condition = []
        clause = ''
        if 'id' in fields:
            condition.append(f'id = {fields["id"]}')
        if 'value' in fields:
            condition.append(f"value = '{fields['value']}'")
        if 'timestamp' in fields:
            condition.append(f'timestamp = {fields["timestamp"]}')
        if len(condition) > 0:
            where = 'WHERE ' + str.join(' AND ', condition)
        if limit:
            clause += f'LIMIT {limit} '
        if offset:
            clause += f'OFFSET {offset} '
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name} {where} {clause};'
                           )
            for record in cursor.fetchall():
                records.append({"id": record[0], "value": record[1],
                               "timestamp": record[2]})
            print(f'Received {len(records)} records from DB')
        except Error as e:
            error = f'DB error: {e.pgerror} {e.diag}'
            print(error)
            result = False
        finally:
            cursor.close()
            return (result, error, records)
