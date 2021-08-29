import re
import time
import random

import yaml

from elmabot import settings
from elmabot.modules import ElmaBotTwitter


with open(settings.FILE_STRINGS_PATH) as strings_file:
    strings = yaml.safe_load(strings_file)

DEFAULT_LANGUAGE = 'en'  # TODO: Use guest user's language
DIALOGS = strings[DEFAULT_LANGUAGE]['dialogs']
COMMANDS = strings[DEFAULT_LANGUAGE]['commands']
MESSAGES = strings[DEFAULT_LANGUAGE]['messages']

TWEETS = {
    'interval': 60*60*1,
    'result': '',
}

BLOGS = {
    'interval': 60*60*6,
    'result': '',
}

TwitterInstance = ElmaBotTwitter(
    settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)


def get_dialog(name):
    dialogs = DIALOGS[name]
    return random.choice(dialogs)


def get_latest_blogs():
    global BLOGS
    result = BLOGS['result'] or ''
    return result


def get_cached_tweets():
    global TWEETS
    result = TWEETS['result'] or ''

    if not result or time.time() - TWEETS['interval'] > 60*60*1:
        result = ''
        # TODO: what if the tweets are protected?
        for tweet in TwitterInstance.get_my_tweets():
            result += tweet.full_text.replace('\n', ' ') + '\n'
            result += '`⭐️ ' + str(tweet.favorite_count) + ' · '
            result += '🔁 ' + str(tweet.retweet_count) + ' · '
            result += tweet.created_at.strftime('%d/%m/%Y')
            result += '`\n\n'
        TWEETS = {'interval': time.time(), 'result': result}
    return result


def get_answer(name, event=None):
    """
    Return the given command if exists
    or return an error message with a list of commands
    """
    answer_data = {
        'tweets': get_cached_tweets(),
        'blogs': get_latest_blogs(),
        'additional': '— __(soon)__',
    }
    result = generate_commands_list(MESSAGES['invalid_command'])
    command = COMMANDS.get(name)
    if command:
        result = command['answer'].format(**answer_data)
    return result


def get_pattern(name):
    _dialogs = DIALOGS[name]
    dialogs = '|'.join([r'\b%s\b' % re.escape(dialog) for dialog in _dialogs])
    return re.compile(dialogs, flags=re.IGNORECASE)


def generate_commands_list(result=""):
    for command, attrs in COMMANDS.items():
        result += "**%s** — __%s__\n" % (command, attrs['description'])
    return result.strip()
