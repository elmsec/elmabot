from random import choice

from elmabot import elmabot, settings


NOT_FOUND_ERROR = (
    "__No documentation found for the given plugin name.__ "
)
DOCS_MESSAGE = (
    "You can use this command to see the documentation of a plugin.\n\n"
    "**Here's a list of the loaded plugins below:**\n{plugin_list}\n\n"
    "**Usage:** `.help <plugin_name>`\n"
    "**For instance:** `.help {random_plugin}`"
)


@elmabot.handle(outgoing=True, pattern=r'^.help(\s(\w+))?')
async def helper(event):
    """
    `.help <opt:plugin_name>`: Sends the documentation of the given plugin
    name, otherwise shows a list of the plugins.
    """
    input_plugin = event.pattern_match.group(1)
    plugin = input_plugin.strip() if input_plugin else None
    DOCS = settings.PLUGIN_DOCS

    if plugin in DOCS and DOCS[plugin]:
        message = f'**Documentation of the `{plugin}` plugin:**\n\n'
        message += DOCS[plugin]
    else:
        plugin_list = list(DOCS.keys())
        plugin_list_str = '\n'.join([f"· `{p}`" for p in plugin_list])
        message = DOCS_MESSAGE.format(
            plugin_list=plugin_list_str,
            random_plugin=choice(plugin_list))
        if plugin:
            message = NOT_FOUND_ERROR + message
    await event.edit(message)
