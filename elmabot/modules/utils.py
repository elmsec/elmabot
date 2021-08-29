import inspect
from time import time
from math import floor as math_floor
from importlib import import_module

from elmabot.modules import database as db
from elmabot import settings


def get_jobs_as_string(jobs):
    message = "**JOBS:**\n"
    for job in jobs:
        message += "`{status} — {job_id} — {name} — {parser}`\n".format(
            job_id=job['_id'],
            status='▶️' if job['status'] else '⏸',
            parser=job['parser'],
            name=job['name'])
    return message


def is_mongo_alive():
    try:
        settings.MONGODB_CLIENT.server_info()
    except BaseException as e:
        settings.LOGGER.error(f'MongoDB connection has failed: {str(e)}')
        return False
    return True


def load_plugins(plugin_list):
    docs = {}
    for plugin_name in plugin_list:
        module = import_module("elmabot.plugins." + plugin_name)
        handlers = inspect.getmembers(module, inspect.isfunction)
        docs.update(load_docs(module, handlers, plugin_name))

    log = "Documentations of {loaded} plugins has been successfully loaded."
    settings.LOGGER.info(log.format(loaded=len(plugin_list)))
    return docs


def load_docs(module, handlers, plugin, docs={}):
    for (name, function) in handlers:
        if getattr(function, '_decorator', None) != 'elmabot.handle':
            continue

        doc = inspect.getdoc(function)
        if doc:
            docstring = doc.replace('\n', ' ')
            docs[plugin] = docs.get(plugin, '')
            docs[plugin] += f"__{docstring}__\n\n" if docstring else ''
    return docs


def humanize_seconds(seconds: int) -> str:
    """
    Convert the given seconds to a human readable time string
    e.g. 182 > 3 minute 2 seconds
    """
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    formatted_seconds = ((str(days) + " gün, ") if days else "") + \
        ((str(hours) + " hours, ") if hours else "") + \
        ((str(minutes) + " mins, ") if minutes else "") + \
        ((str(seconds) + " secs") if seconds else "")
    return formatted_seconds


def humanize_bytes(size):
    """
    Convert the given integer variable in bytes
    to a human readable format
    """
    if not size:
        return ""
    power = 2**10  # 1024
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def is_first_message(e):
    sender = await e.get_sender()
    return e.is_private and db.User.get_or_create_user(sender)[1] is True


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """
    Generic progress_callback
    """
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        progress_str = "[{0}{1}]\nProgress: {2}%\n".format(
            ''.join(["█" for i in range(math_floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math_floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress_str + \
            "{0} / {1}\nRemaining time: {2}".format(
                humanize_bytes(current),
                humanize_bytes(total),
                humanize_seconds(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nFilename: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def replace_special_characters(content):
    CHARMAP = {
        ord(u'ş'): u's',
        ord(u'Ş'): u'S',
        ord(u'ı'): u'i',
        ord(u'İ'): u'I',
        ord(u'ç'): u'c',
        ord(u'Ç'): u'C',
        ord(u'ü'): u'u',
        ord(u'Ü'): u'U',
        ord(u'ö'): u'o',
        ord(u'Ö'): u'O',
        ord(u'ğ'): u'g',
        ord(u'Ğ'): u'G',
    }
    result = ''.join(map(lambda c: CHARMAP.get(ord(c), c), content))
    return result
