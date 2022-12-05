import hashlib
from django.conf import settings


def md5(data_string, mod):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    if mod == 1:
        obj.update(data_string)
    elif mod == 2:
        obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
