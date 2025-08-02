import pandas as pd
import cx_Oracle
from secrets_retrieval import get_password


class oracle_query():
    def __init__(self):
        self.password = get_password('/home/s2630332/gfs/ApiKeys/database.txt')
        self.conn = cx_Oracle.connect(user="s2630332", password=self.password, dsn="geosgen")
# Get the db password
    def query(self):
        self.df = pd.read_sql("SELECT NAME, INTRODUCTION FROM ops$scotgaz.towns WHERE SEQNO = 40", self.conn)
        pd.set_option('display.max_colwidth', None)
        print(self.df)
