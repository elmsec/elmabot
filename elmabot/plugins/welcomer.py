from telethon import events

from elmabot import elmabot
from elmabot.plugins.partials import (
    get_dialog_items,
    get_random_dialog_item,
    get_pattern,
    generate_commands_list,
)
from elmabot.modules import is_first_message


MSG_WELCOME = get_dialog_items('greetings_answers')[0].format(
    commands_list=generate_commands_list())


@elmabot.handle(private_only=True, incoming=True, func=is_first_message)
async def first_message_handler(event):
    await event.reply(MSG_WELCOME, link_preview=False)
    raise events.StopPropagation  # stop execution of other handlers


@elmabot.handle(
    private_only=True, incoming=True, pattern=get_pattern('greetings'))
async def greeting_handler(event):
    random_message = get_random_dialog_item('greetings_answers').format(
        commands_list=generate_commands_list())
    await event.reply(random_message, link_preview=False)
