import os

LOGGER = None
DEBUG = bool(os.getenv('DEBUG', False))  # TODO: will not work :D
CURRENT_LANG = os.getenv('CURRENT_LANG', 'tr')

STRING_SESSION = os.getenv('STRING_SESSION')

MONGO = None
MONGODB_CLIENT = None
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_URL = os.getenv('DATABASE_URL')
DB_NAME = os.getenv('DB_NAME', 'elmabot')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))
TELEGRAM_API_ID = os.getenv('API_ID')
TELEGRAM_API_HASH = os.getenv('API_HASH')

# MY_TWITTER_ID = int(os.getenv('TWITTER_ID', 0))
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


# PATHS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.dirname(os.path.join(ROOT_DIR, 'files/'))
PARTIALS_DIR = os.path.dirname(os.path.join(ROOT_DIR, 'plugins/partials/'))

FILE_SESSION = os.path.join(FILES_DIR, 'elmabot')
FILE_STRINGS_PATH = os.path.join(PARTIALS_DIR, 'strings.yaml')
FILE_DB_PATH = os.path.join(FILES_DIR, 'users.db')


# SETTINGS
WHITELIST_DEL = [ADMIN_ID]  # TODO: Use DB instead of this static var


# CONSTANTS
REGEX_FLOAT = '( [0-9]+(.([0-9]+))?)'
PLUGIN_DOCS = dict()
