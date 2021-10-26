import os

configuration = os.environ.get('SETTINGS_CONFIGURATION')

if configuration == 'local':
    from .local import *
else:
    from .base import *
