from telethon import functions
from elmabot import elmabot, settings


@elmabot.handle(outgoing=True, reply_only=True, pattern="^.userid$")
async def get_user_id(event):
    """
    `.userid`: Returns the ID of the user who sent the specified message.
    """
    to = await event.get_reply_message()
    sender = to.sender if not to.forward else to.forward.sender

    user_id = sender.id
    first_name = getattr(sender, 'first_name', getattr(sender, 'title', '—'))
    last_name = getattr(sender, 'last_name', '') or ''
    full_name = f"{first_name} {last_name}".strip()
    name = '@' + sender.username if sender.username == 'x' else full_name

    await event.edit(
        "**Name:** {}\n**User ID:** `{}`".format(name, user_id))


@elmabot.handle(outgoing=True, pattern="^.chatid$")
async def get_chat_id(event):
    """
    `.chatid`: Returns the ID of the current chat.
    """
    result = f"**Chat ID:** `{str(event.chat_id)}`"
    await event.edit(result)


@elmabot.handle(outgoing=True, reply_only=True, pattern="^.messageid$")
async def get_message_id(event):
    """
    `.messageid`: Returns the ID of the replied message.
    """
    to = await event.get_reply_message()
    result = f"**Message ID:** `{str(to.id)}`"
    await event.edit(result)


@elmabot.handle(outgoing=True, pattern=r"^.usernames(\+?)$")
async def list_reserved_usernames(event):
    """
    `.usernames` OR `.usernames+`: Returns the list of your reserved usernames.
    """
    warning = (
        '```it\'s highly dangerous to run this command on another chat. '
        'if you still want to use it, add + to the end of the command.```'
    )

    plus = event.pattern_match.group(1) == '+'
    if event.chat_id != settings.ADMIN_ID and not plus:
        return await elmabot.rollback(event, warning, seconds=5)

    result = await elmabot(
        functions.channels.GetAdminedPublicChannelsRequest())

    message = ""
    for channel in result.chats:
        message += f"🚩 {channel.title} @{channel.username} \n"
    await event.edit(message)


@elmabot.handle(outgoing=True, pattern='.own_left_channels')
async def own_left_channels(event):
    """
    `.own_left_channels`: Shows a list of your own channels you've left.
    In order to join one of these channels, use `.join_own_left_channel <ID>`
    from the chat module.
    """
    async with elmabot.takeout() as takeout:
        left_channels = await takeout(
            functions.channels.GetLeftChannelsRequest(0))

        channels = [c for c in left_channels.chats if c.creator]
        channel_list = "**THE CHANNELS I LEFT:**\n\n"
        for channel in channels:
            channel_list += f'`{channel.id}` - {channel.title}\n'
        await event.edit(channel_list)
