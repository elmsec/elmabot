import asyncio

# from telethon import functions
from telethon.tl.functions.channels import (
    JoinChannelRequest, LeaveChannelRequest, GetLeftChannelsRequest
)

from elmabot import elmabot


@elmabot.handle(outgoing=True, pattern=r"^.quit$")
async def leave_chat(event):
    """
    `.quit`: Leaves the current chat.
    """
    await event.edit("`Leaving the chat...`")
    try:
        await elmabot(LeaveChannelRequest(event.chat_id))
        await asyncio.sleep(3)
        await event.delete()
    except TypeError:
        await elmabot.rollback(event, '`I could not leave...`')


@elmabot.handle(outgoing=True, pattern='.join_own_left_channel ([0-9]+)')
async def join_own_left_channels(event):
    """
    `.join_own_left_channel <channel_id>`: Join to the channel specified with
    the <channel_id>. You can obtain this ID with the `.own_left_channels`
    command from the info module. See `.help info`.
    """
    channel_id = event.pattern_match.group(1)
    message = '`You joined back the channel {id} - {title}`'
    warning = (
        '`After the command, a channel ID should be specified. You can use '
        'the ".own_left_channels" command to get channel IDs.`'
    )
    if not channel_id:
        return await elmabot.rollback(event, warning)

    async with elmabot.takeout() as takeout:
        left_channels = await takeout(
            GetLeftChannelsRequest(0))

        channels = [c for c in left_channels.chats if c.creator]
        for channel in channels:
            if channel.id == int(channel_id):
                await takeout(JoinChannelRequest(channel))
                return await event.edit(
                    message.format(id=channel.id, title=channel.title))
