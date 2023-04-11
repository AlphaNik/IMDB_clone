import os
from dotenv import load_dotenv
load_dotenv()

class Constant:
    SECRET_KEY = os.getenv('SECRET_KEY')
   