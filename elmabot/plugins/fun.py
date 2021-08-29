import asyncio
from random import shuffle

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events

from elmabot import elmabot, settings

"""
HELPS TO MAKE CHATS FUN AND EASY
"""

REGEX_FLOAT = settings.REGEX_FLOAT
RANDOMS = [
    'AHSDGAHSDHASDGHASHGD', 'ASDHJGASDGASHDGAHSGHSD', 'ASDGHASDHGASHGASHD',
    'HAHSAHASDHASDH', 'ASFSDAFASDASFSD', 'ASHDGHAGSDHJSDGSAGDJH',
    'ASHSDAHASDHGASHD', 'AMSAKSAJSAJSAJ', 'WQJGWJQEWEHGHEWGHWEGH',
    'JSADHJADSHASDHSDH', 'ASHJDHASDHASDHJASDH', 'HASDGHSADGHSADGHSAD',
    'LASNASNSANSJASDJ', 'ASASHDASHSADGRGI', 'ASJDGASDHJGAHSDHASDHASHASD',
]


@elmabot.handle(outgoing=True, pattern=r'^.haha(ha*)?')
async def random_laugh(event):
    """
    `.haha<ha*>`: Send random set of characters as much as occurrences of the
    'ha' values in the given string. If the message is a reply, then the first
    one will be sent as a reply to that message.
    """
    await event.delete()
    count = event.raw_text.count('ha')
    reply = await event.get_reply_message()

    randoms = sorted(RANDOMS)
    shuffle(randoms)

    for random in randoms[:int(count)]:
        if reply and randoms[0] == random:
            await reply.reply(random)
        else:
            await event.respond(random)
        await asyncio.sleep(1)


@elmabot.handle(outgoing=True, pattern=r'^.yell (.+?)' + REGEX_FLOAT + '?$')
async def aggressive_sayings(event):
    """
    `.yell <text> <opt:interval>`: Send the given text as __T E X T__ with a
    typewriter effect. The interval is set to 0.3 by default.
    """
    say = event.pattern_match.group(1)
    interval = event.pattern_match.group(2) or 0.3

    current_say = ''
    for letter in say:
        current_say += letter.upper() + ' '

        if letter.strip():
            await event.edit(current_say)

        await asyncio.sleep(float(interval))


@elmabot.handle(outgoing=True, pattern='.asciiphoto', reply_only=True)
async def ascii_photo_generator(event):
    """
    `.asciiphoto`: Converts the photo of the replied message to an
    ascii-style photo.
    """
    chat = "@asciiart_bot"
    reply_message = await event.get_reply_message()

    if not reply_message.media:
        return await elmabot.rollback(event, '`like there\'s no photo...`')

    await event.edit('`creating an artwork...`')
    async with elmabot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164766745)
            )
            await elmabot.send_message(chat, reply_message)
        except YouBlockedUserError:
            return await event.edit("Looks like you blocked @asciiart_bot`")
        else:
            response = await response
            await elmabot.send_file(event.chat_id, response.message.media)
            await event.delete()
