import importlib
import re
import logging

_routers = {}
_middlewares = {}

def _resolve_handler(handler):
    return re.match('(^\w[\w\.]+)@(\w+)', handler).groups()

def _get_router(router):
    global _routers
    return _routers.get(router)

class router:
    def __init__(self, name, handler):
        module, method = _resolve_handler(handler)
        self._name = name
        self._handler = getattr(importlib.import_module(module), method)

    def register(self):
        global _routers
        _routers[self._name] = {
            'name': self._name,
            'handler': self._handler,
            'rules': {}
        }
        
class middleware:
    def __init__(self, name, handler):
        module, method = _resolve_handler(handler)
        self._name = name
        self._handler = getattr(importlib.import_module(module), method)
           
    def register(self):
        global _middlewares
        _middlewares[self._name] = {
            'name': self._name,
            'handler': self._handler
        }

class rule:
    def __init__(self, router):
        self._router = router
        self._before = []
        self._after = []

    def route(self, url, handler):
        module, method = _resolve_handler(handler)
        self._url = url
        self._type = 'router' if module == 'router' else 'handler'
        self._next_router = method
        self._handler = getattr(importlib.import_module(module), method) if module != 'router' else handle
        return self

    def register(self):
        router = _get_router(self._router)
        router['rules'][self._url] = {
            'router': self._router,
            'url': self._url,
            'type': self._type,
            'next_router': self._next_router,
            'handler': self._handler,
            'after': self._after,
            'before': self._before,
        }

    def before_process(self, middleware_list):
        self._before = middleware_list
        return self

    def after_process(self, middleware_list):
        self._after = middleware_list
        return self



def handle(e):
    r = _get_router(e['LOCODE_ROUTER'])
    r.get('handler')(e)
    rule = get_routing_rule(e)
    if rule is None:
        return False

    for middleware in rule.get('before'):
        if not _middlewares.get(middleware).get('handler')(e):
            return

    if rule.get('type') == 'router':
        e['LOCODE_ROUTER'] = rule.get('next_router')

    if not rule.get('handler')(e):
        return

    for middleware in rule.get('after'):
        if not _middlewares.get(middleware).get('handler')(e):
            return

def set_routing_rule(e, rule):
    e['LOCODE_ROUTING_RULE'] = rule

def get_routing_rule(e):
    r = _get_router(e['LOCODE_ROUTER'])
    rules = r.get('rules')
    return rules.get(e.get('LOCODE_ROUTING_RULE')) 
