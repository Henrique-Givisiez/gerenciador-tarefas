import pymysql

class BaseHelper:
    def __init__(self, connection: pymysql.connections.Connection, cursor: pymysql.cursors.Cursor):
        self.conn = connection
        self.cursor = cursor

        