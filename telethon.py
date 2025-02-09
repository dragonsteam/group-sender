from telethon.sync import TelegramClient  # Uses sync version
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "sync_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Start client (no 'await' needed)
client.start()
print(f"Logged in! Session saved as '{SESSION_NAME}.")
