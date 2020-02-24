import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TRACK_TOKEN = os.getenv("TRACK_TOKEN")
WHEATHER_TOKEN = os.getenv("WHEATHER_TOKEN")
