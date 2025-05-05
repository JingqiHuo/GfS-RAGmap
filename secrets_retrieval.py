import sys
import logging
from pathlib import Path
import os

def get_APIkey(passfile):
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
get_password = get_APIkey
