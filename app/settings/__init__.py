# -*- coding: utf-8 -*-
import os
import sys
from split_settings.tools import optional, include

# reference to absolute paths for later use
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
APP_ROOT = os.path.join(SITE_ROOT, 'app')

# add app path
sys.path.insert(0, APP_ROOT)

#
gettext = lambda s: s
_ = gettext

# dev & test
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

include(
    'components/base.py',
    'components/template.py',
    'components/storage.py',

    # optional local settings
    optional(os.path.join(APP_ROOT, 'local_settings.py')),

    # via server based settings in etc (placed by ansible deployment tasks)
    optional('/etc/mixdown-api/application-settings.py'),
    optional('/etc/mixdown-api/logging.py'),
    scope=locals()
)
