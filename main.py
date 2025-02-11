import os
from dotenv import load_dotenv
from telethon import utils
from telethon.sync import TelegramClient  # Uses sync version

# Load environment variables
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# client.start()

PHONE = "+998901558090"
# SESSION_NAME = "sync_session"
SESSION_NAME = "sessions/" + utils.parse_phone(phone=PHONE)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

if not client.is_connected():
    client.connect()
else:
    print('Already connected')

# result = client.send_code_request(phone=PHONE)
# print(result)
# print(result.phone_code_hash)

client._phone_code_hash = {'998901558090': '967f16199eb7d4647f'}
me = client.sign_in(phone=PHONE, code="34025")
print(me)


# me = client.get_me()
# print(me)


# async def sing_in():
#     await self.connect()

#     try:
#         result = await self(functions.auth.SendCodeRequest(
#             phone, self.api_id, self.api_hash, types.CodeSettings()))
#     except Exception as e:
#         print(e)


# print(f"Logged in! Session saved as '{SESSION_NAME}.")
