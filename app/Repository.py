import mysql.connector

users_query = 'select * from Users where Users.username="%s"'


class AppRepository:
    def __init__(self):
        pass

    @staticmethod
    def connect() -> mysql.connector:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                username='networktest',
                password='test',
                port='8889',
                database='licenta'
            )
            return connection
        except mysql.connector.InterfaceError:
            print('Interface error when connecting to mysql')
            exit(1)

    def search_by_username(self, username):
        connection = self.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(users_query % username)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as ex:
            print(ex)
        finally:
            if connection:
                connection.close()
        return {}

    def search_by_prediction_name(self, prediction):
        return self.execute_query('SELECT * FROM users where Users.network_name="%s"' % prediction)
        # connection = self.connect()
        # try:
        #     cursor = connection.cursor()
        #     cursor.execute('SELECT * FROM users where Users.network_name="%s"' % prediction)
        #     result = cursor.fetchall()
        #     return result
        # except Exception as ex:
        #     print(ex)
        # finally:
        #     if connection:
        #         connection.close()
        # return {}

    def find_all_users(self):
        return self.execute_query("SELECT * FROM users")

    def execute_query(self, query):
        connection = self.connect()
        result = {}
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            if connection:
                connection.close()
        return result
