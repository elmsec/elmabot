from telethon import events

from elmabot import elmabot
from elmabot.plugins.partials import (
    get_dialog,
    get_pattern,
    generate_commands_list,
)
from elmabot.modules import is_first_message


MSG_WELCOME = get_dialog('greetings_answers').format(
    commands_list=generate_commands_list())


@elmabot.handle(private_only=True, incoming=True, func=is_first_message)
async def first_message_handler(event):
    await event.reply(MSG_WELCOME, link_preview=False)
    raise events.StopPropagation  # stop execution of other handlers


@elmabot.handle(
    private_only=True, incoming=True, pattern=get_pattern('greetings'))
async def greeting_handler(event):
    await event.reply(MSG_WELCOME, link_preview=False)
