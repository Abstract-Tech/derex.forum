from .derex import *  # noqa

COMMENTS_SERVICE_URL = "http://forum:4567"
COMMENTS_SERVICE_KEY = "forumapikey"

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True  # type: ignore # noqa: F405
