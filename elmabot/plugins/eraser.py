from elmabot import elmabot
from time import time


@elmabot.handle(outgoing=True, reply_only=True, pattern=".del( self)?$")
async def del_below(event):
    """
    `.del <opt:self>`: Delete all the messages by starting from the reply.
    If the argument <self> is given, only deletes the messages sent by you.
    """
    chat = await event.get_input_chat()
    is_self = event.pattern_match.group(1)
    from_user = is_self.strip() if is_self else None
    iteration = event.client.iter_messages(
        chat, min_id=event.reply_to_msg_id, from_user=from_user)

    messages = [message.id async for message in iteration]
    messages.append(event.reply_to_msg_id)

    await event.client.delete_messages(chat, messages)


LAST_MESSAGES = dict()


@elmabot.handle(private_only=True)
async def history_eraser(event):
    """
    `<< history_eraser >>`
    This handler runs automatically on every outgoing message to keep the chat
    clean. For bot sides, it deletes all messages except the last n message.
    'n' is an integer defined by you, see `history_limit` below.
    """
    global LAST_MESSAGES
    # number of recent messages to keep;
    # other messages will be deleted
    history_limit = 30
    spam_threshold = 60

    last_message = LAST_MESSAGES.get(event.chat_id)
    if last_message and time() - last_message < spam_threshold:
        return

    chat = await event.get_input_chat()
    older_messages = event.client.iter_messages(chat, add_offset=history_limit)
    messages = [message_id async for message_id in older_messages]

    await event.client.delete_messages(chat, messages)
    LAST_MESSAGES[event.chat_id] = time()
