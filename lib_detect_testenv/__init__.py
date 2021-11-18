# add_to_init{{{
# __init__.py :
# detect test environment and add path for local testing
from .lib_detect_testenv import *

if is_doctest_running():
    add_path_to_syspath(__file__)
# add_to_init}}}

# put Your imports here


# __init__conf__ needs to be imported after Your imports, otherwise we would create circular import on the cli script,
# which is reading some values from __init__conf__
from . import __init__conf__

__title__ = __init__conf__.title
__version__ = __init__conf__.version
__name__ = __init__conf__.name
__url__ = __init__conf__.url
__author__ = __init__conf__.author
__author_email__ = __init__conf__.author_email
__shell_command__ = __init__conf__.shell_command
