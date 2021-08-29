import logging
from pymongo import MongoClient

from telethon.sessions import StringSession

from elmabot import settings
from elmabot.modules.elmabot_client import ElmaBotClient
from elmabot.modules.utils import load_plugins
from elmabot.plugins import PLUGIN_LIST


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ],
)

settings.LOGGER = logging.getLogger(__name__)

elmabot_session = (
    settings.FILE_SESSION
    if settings.DEBUG
    else StringSession(settings.STRING_SESSION))

elmabot = ElmaBotClient(
    elmabot_session,
    settings.TELEGRAM_API_ID,
    settings.TELEGRAM_API_HASH)

settings.PLUGIN_DOCS.update(load_plugins(PLUGIN_LIST))


settings.MONGODB_CLIENT = MongoClient(settings.MONGODB_URI)
settings.MONGO = (
    settings.MONGODB_CLIENT.dev
    if settings.DEBUG else settings.MONGODB_CLIENT.elmabot
)
