import logging
import sys
from functools import wraps
import log.client_log_config
import log.server_log_config
import time
sys.path.append('..')

def log_data(func):
    called_module = sys.argv[0].split('/')
    @wraps(func)
    def decorated_log(*args, **kwargs):
        if 'server.py' in called_module:
            result = func(*args, **kwargs)
            logger_server = logging.getLogger('log_server')
            logger_server.debug(f'Была вызвана функция {func.__name__} с атрибудами {args}, {kwargs}, {time.ctime(time.time())} Функция вызвана из модуля {func.__module__}')
            return result

        if 'client.py' in called_module or 'client2.py' in called_module:
            result = func(*args, **kwargs)
            logger = logging.getLogger('log_client')
            logger.debug(
                f'Была вызвана функция {func.__name__} с атрибудами {args}, {kwargs}, {time.ctime(time.time())} Функция вызвана из модуля {func.__module__}')
            return result

    return decorated_log