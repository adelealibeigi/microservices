from dotenv import dotenv_values
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

config = dotenv_values(BASE_DIR / '.secret_keys')
HOST = config['HOST']
PORT = config['PORT']
PASSWORD = config['PASSWORD']

