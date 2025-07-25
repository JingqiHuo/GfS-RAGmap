import pandas as pd
import cx_Oracle
from secrets_retrieval import get_password
from config.config import *

class oracle_query():
    def __init__(self):
        self.password = get_password(DB_PASSWORD_PATH)
        self.conn = cx_Oracle.connect(user=DB_USER, password=self.password, dsn=DB_DSN)
# Get the db password
    def query(self):
        self.df = pd.read_sql("SELECT NAME, INTRODUCTION FROM ops$scotgaz.towns WHERE SEQNO = 40", self.conn)
        pd.set_option('display.max_colwidth', None)
        print(self.df)
