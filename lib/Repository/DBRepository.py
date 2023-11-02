from abc import ABC
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

class DBRepository(ABC):

    __cursor: MySQLCursor
    __db: MySQLConnection

    def __init__(self, host, port, user, password, database) -> None:
        self.__db = mysql.connector.connect(
            host = host,
            port = port,
            database = database,
            user = user,
            password = password
        ) 

        self.__cursor = self.__db.cursor()

    def find(self, find_options):
        # {select: ["column"], from: "table", where: [{"column": "equal"}]}
        query = ""
        if find_options.get("select"):
            query += self.__processSelect(find_options["select"])
        
        else:
            query += "SELECT * "

        if find_options.get("from"):
            query += self.__processFrom(find_options["from"])
        
        else:
            raise Exception("From option is required!")
        
        if find_options.get("where"):
            query += self.__processWhere(find_options["where"])

        x = self.__execQuery(query, find_options["select"])
        return x


    def add(self, insert_options):
        # {"insert": [{"column", "value"}], "into": "table"}

        if not(insert_options.get("insert")) and not(insert_options.get("into")):
            raise Exception("Insert and into option is required")
        
        query = self.__processInsert(insert_options["insert"], insert_options["into"])

        self.__cursor.execute(query)
        self.__db.commit()
        return self.__cursor.lastrowid
    
    def createTable(self, table_name: str, columns: list):
        query = f"CREATE TABLE {table_name} ("

        for index, column in enumerate(columns):
            query += f" {column} varchar(255)"
            if index < len(columns) - 1:
                query += ", "

        query += ")"

        try:
            self.__cursor.execute(query)
        except:
            print("Warning: Table already exists!")
            print("Dropping table...")
            self.__dropTable(table_name)
            self.__cursor.execute(query)

        self.__db.commit()

    def __dropTable(self, tableName: str):
        query = f"DROP TABLE {tableName}"
        try:
            self.__cursor.execute(query)
        except:
            print("Warning: Table not exists!")

        self.__db.commit()

    def __processInsert(self, insert_options, table: str):

        valuesList = []

        query = "INSERT INTO "
        query += table
        query += " ("

        for index, column_option in enumerate(insert_options):
            key = list(column_option.keys())[0] #?????
            valuesList.append(column_option[key])
            query += key
            if index < len(insert_options) - 1:
                query += ", "

            
        query += ") "

        query += "VALUES ("
        for index, value in enumerate(valuesList):
            query += "%s"
            if index < len(valuesList) - 1:
                query += ", "

        query += ")"
        
        # print(query % tuple(valuesList))
        return query % tuple(valuesList)

    def __execQuery(self, query, select_options: list):
        self.__cursor.execute(query)
        resFetch = self.__cursor.fetchall()

        return self.__mapFetchResponse(resFetch, select_options)
        
    
    def __mapFetchResponse(self, fetch_data, select_options):
        resList = []

        for row in fetch_data:
            rowDict = {}
            for index, key in enumerate(select_options):
                rowDict[key] = row[index]
            resList.append(rowDict) 
        
        return resList


    def __processSelect(self, select_options: list):
        query = "SELECT " 
        for index, column in enumerate(select_options):
            query += column + " "

            if index < len(select_options) - 1:
                query += ","

        return query

    def __processFrom(self, from_options: str):
        return "FROM " + from_options

    def __processWhere(self, where_options: list):
        query = "WHERE "
        for index, column in enumerate(where_options):
            key = column.keys()
            query += key + " = " + column[key]
            if len(where_options) > 1 and index != len(where_options) - 1:
                query += " AND "

        return query