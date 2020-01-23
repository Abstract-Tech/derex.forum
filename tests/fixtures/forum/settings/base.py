import os


SERVICE_VARIANT = os.environ["SERVICE_VARIANT"]
assert SERVICE_VARIANT in ("lms", "cms")
exec("from {}.envs.derex.base import *".format(SERVICE_VARIANT), globals(), locals())

# Id of the site fixture to use, instead of looking up the hostname
SITE_ID = 1

COMMENTS_SERVICE_URL = 'http://forum:4567'
COMMENTS_SERVICE_KEY = 'forumapikey'

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
