from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# from sqlalchemy_utils import create_database, database_exists


url_object = URL.create(
    "postgresql",
    username = "*",
    password = "*@!",  # plain (unescaped) text
    host     = "5432",
    database = "financial"  )

engine = create_engine(url_object)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

Base = declarative_base()



from psycopg2 import pool
import psycopg2


CenterDB_user     = "*"
CenterDB_password = "*"
CenterDB_host     = "*"
CenterDB_port     = "5432"
CenterDB_database = "financial"


class QueryDbClass():
    def __init__(self):
        self.connection, self.cursor = self.connect2CenterDb()

    def connect2CenterDb(self):
        db = psycopg2.pool.ThreadedConnectionPool(minconn=1,
                                                  maxconn=10000,
                                                  # idle_timeout  = 10 * 60 , # default value
                                                  user         = CenterDB_user,
                                                  password     = CenterDB_password,
                                                  host         = CenterDB_host,
                                                  port         = CenterDB_port,
                                                  database     = CenterDB_database)
        connection = db.getconn()
        cursor     = connection.cursor()

        return connection, cursor


    def checkDbConnection(self):
        try:
            self.cursor.execute("select 1 ")
        except:
            self.connection, self.cursor = self.connect2CenterDb()


    def checkDbConnectionDecorator(self, func):
        def wrapper_dbChecker(*args, **kwargs):
            self.checkDbConnection()
            value = func(*args, **kwargs)
            return value

        return wrapper_dbChecker

    # @checkDbConnection
    def executeQuery(self,
                     query,
                     is_commit = False):
        if type(query) != str:
            print(" invalid qery type ")
            return

        self.cursor.execute(query)

        if is_commit:
            self.connection.commit()

        rows = self.cursor.fetchall()

        return rows


    # Calling destructor
    def __del__(self):
        self.cursor.close()
        self.connection.close()
#

class Db():
    def __init__(self):
        self.connection, self.cursor = self.connect2CenterDb()

    def connect2CenterDb(self):
        cursor = engine.connect()
        return engine, cursor

    def checkDbConnection(self):
        try:
            self.cursor.execute("select 1 ")
        except:
            self.connection, self.cursor = self.connect2CenterDb()

    def __del__(self):
        pass
        # self.cursor.close()
        # self.connection.close()
