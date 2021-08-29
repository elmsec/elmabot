from asyncio import sleep as async_sleep
from functools import wraps

from telethon import TelegramClient, events

from elmabot import settings


class ElmaBotClient(TelegramClient):
    def __init__(self, *args, **kwargs):
        kwargs['flood_sleep_threshold'] = 60
        super(ElmaBotClient, self).__init__(*args, **kwargs)

    async def rollback(self, event, message, seconds=3):
        """
        Show the specified message, wait <seconds> seconds and delete
        the sent/edited message.

        Mostly used to show an error and then destroy the message.
        """
        await event.edit(message)
        await async_sleep(seconds)
        await event.delete()

    def handle(self, **kwargs):
        """
        Custom decorator to make the given function a handler.
        """
        IS_DEBUG = settings.DEBUG

        # Extra keyword (arguments) that will be checked
        arguments = [
            'allow_forward',
            'groups_only',
            'private_only',
            'reply_only',
            'allow_bots',
        ]
        # Distinguish extra keywords arguments
        kwargs_ext = {
            k: kwargs.pop(k, None)
            for k, v in kwargs.copy().items() if k in arguments}

        pattern = kwargs.get('pattern', '')
        if type(pattern) is str and pattern.startswith('^.'):
            kwargs['pattern'] = pattern.replace('^.', '^[.]')

        if IS_DEBUG:
            # remove restriction on the admin account so it can test handlers
            # of user commands (incoming) with own messages (outgoing)
            kwargs['incoming'] = None

        def decorator(func):
            # Set the _decorator attribute to identify handlers in order to
            # generate help documents from
            func._decorator = 'elmabot.handle'

            @wraps(func)
            async def wrapper(event):
                # Possible conflicts to check and return away if any
                problem = (
                    IS_DEBUG and (not event.out and not event.is_private),
                    (kwargs_ext.get('private_only') and not event.is_private),
                    (kwargs_ext.get('groups_only') and not event.is_group),
                    (not kwargs_ext.get('allow_forward') and event.fwd_from),
                )

                if any(problem):
                    return

                if kwargs_ext.get('reply_only') and not event.reply_to_msg_id:
                    return await self.rollback(event, '`Mesaj belirtilmedi.`')

                is_bot = getattr((await event.get_sender()), 'bot', None)
                if not kwargs_ext.get('allow_bots') and is_bot:
                    return

                await func(event)

            self.add_event_handler(wrapper, events.NewMessage(**kwargs))
            return wrapper
        return decorator
