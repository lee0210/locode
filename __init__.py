print('initializing router')
import config.router
print('initializing resource')
import config.resource

def is_empty(o):
    if isinstance(o, (list, dict)):
        return len(o) == 0
    raise TypeError('error type')
