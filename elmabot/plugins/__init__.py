
import glob
from os.path import dirname, basename, isfile, join


plugins = glob.glob(join(dirname(__file__), "*.py"))

ENABLED_PLUGINS = [  # please keep the order alphabetic
    'analyzer',
    'chat',
    # 'eraser',
    # 'exclamations',
    'fun',
    'help',
    'info',
    # 'jobs',
    'promessage',
    # 'welcomer',
]
PRIORITIZED_PLUGINS = ['welcomer', 'exclamations']
PLUGIN_LIST = [
    basename(f)[:-3] for f in plugins
    if isfile(f) and not f.endswith('__init__.py')
    and basename(f)[:-3] in ENABLED_PLUGINS]
PLUGIN_LIST.sort(
    key=lambda n: (PRIORITIZED_PLUGINS.index(n), n)
    if n in PRIORITIZED_PLUGINS else (10**10, n))

__all__ = PLUGIN_LIST
