import pandas as pd
import cx_Oracle
from secrets_retrieval import get_password

    
# Get the db password
password = get_password('E:\GfS-RAG-Map-Return\ApiKeys\database.txt')


conn = cx_Oracle.connect(user="s2630332", password=password, dsn="geosgen")
df = pd.read_sql("SELECT NAME, INTRODUCTION FROM ops$scotgaz.towns", conn)
pd.set_option('display.max_colwidth', None)
print(df)
