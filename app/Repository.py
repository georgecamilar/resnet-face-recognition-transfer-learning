import mysql.connector

users_query ='select * from Users where Users.username="%s"'
class AppRepository:
    def __init__(self):
        # self._connection = self.connect()
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
            return result
        except Exception as ex:
            print(ex)
        return {}
