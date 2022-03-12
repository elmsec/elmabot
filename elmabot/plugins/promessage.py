import asyncio

from elmabot import elmabot


@elmabot.handle(outgoing=True, pattern=r'^.sd (\d+) (.+)')
async def self_destruct_message(event):
    """
    `.sd <seconds> <text>`: Sends a self-destructing message.
    """
    counter = event.pattern_match.group(1)
    message = event.pattern_match.group(2)

    await event.edit(message)
    await asyncio.sleep(int(counter))
    await event.delete()


@elmabot.handle(outgoing=True, pattern="^.edit (.+)")
async def editer(event):
    """
    `.edit <text>`: Edits your message you've replied to with the given text.
    """
    text = event.pattern_match.group(1)
    to = await event.get_reply_message()

    if not to:
        return await event.edit('`No text specified.`')

    await to.edit(text)
    await event.delete()


@elmabot.handle(outgoing=True, reply_only=True, pattern=r"^.fw( \d+)?")
async def forwarder(event):
    """
    `.fw <opt:limit>`: Forwards messages by starting from the message you've
    replied to. <limit> is the number of messages that will be forwarded.
    """

    _limit = event.pattern_match.group(1)
    limit = int(_limit) if _limit else None
    chat = await event.get_input_chat()

    # delete '.fw' message to avoid forwarding it
    await event.delete()

    iteration = event.client.iter_messages(
        chat,
        min_id=event.reply_to_msg_id-1,
        limit=limit,
        reverse=True)

    messages = [message async for message in iteration]
    await event.client.forward_messages(await event.get_sender(), messages)
