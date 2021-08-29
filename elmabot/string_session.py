import settings
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

with TelegramClient(
        StringSession(),
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH) as elmabot:
    print(elmabot.session.save())
