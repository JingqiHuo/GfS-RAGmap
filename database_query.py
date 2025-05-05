import pandas as pd
import cx_Oracle
import sys
import logging
from pathlib import Path
import os
def get_password(passfile='databasepassword.txt'):
    """
    Reads the database password from a specified file.

    Args:
        passfile (str): The file name where the password is stored.

    Returns:
        str: The password read from the file.

    Raises:
        SystemExit: If the password file is not found.
    """
    home = Path.home()
    passfile = os.path.join(home, passfile)
    try:
        with open(passfile) as file:
            pw = file.readline().strip()
        return pw
    except FileNotFoundError as detail:
        logging.error(f'Password file not found: {detail}')
        sys.exit()
    
# Get the db password
password = get_password()


conn = cx_Oracle.connect(user="s2630332", password=password, dsn="geosgen")
df = pd.read_sql("SELECT NAME, INTRODUCTION FROM ops$scotgaz.towns", conn)
pd.set_option('display.max_colwidth', None)
print(df)
