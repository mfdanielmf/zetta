from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# LÍMITES
DEFAULT_RATE_LIMIT = "100/minute"
AUTH_RATE_LIMIT = "20/minute"
UPLOAD_RATE_LIMIT = "20/minute"
FILE_RATE_LIMIT = "30/minute"
