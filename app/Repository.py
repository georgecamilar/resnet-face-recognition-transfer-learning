import mysql.connector


class AppRepository:
    def __init__(self):
        # self._connection = self.connect()
        pass

    @staticmethod
    def connect() -> mysql.connector:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                username='root',
                password='george'
            )
            return connection
        except mysql.connector.InterfaceError:
            print('Interface error when connecting to mysql')
            exit(1)

    def search_cookie(self, id):
        try:
            if self._connection.connection_id is True:
                with self._connection.cursor() as cursor:
                    query = 'SELECT * FROM Sessions WHERE id=%s' % id
                    result = cursor.execute(query)
                    if result is not None:
                        return True
        except Exception as ex:
            print(ex)
        return False
