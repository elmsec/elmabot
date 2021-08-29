from elmabot import elmabot
from elmabot.plugins.partials import get_answer


@elmabot.handle(pattern=r'^!([a-z_]+)')
async def commands_handler(event):
    await event.mark_read()
    await event.reply(get_answer(event.raw_text, event), link_preview=False)
