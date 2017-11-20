# Resource Manager
import types
import importlib
import re

bindings = {}

instances = {}

def __resolve_name(maker_name):
    return re.match('(^\w[\w\.]+)@(\w+)', maker_name).groups()

def __import(maker_name):
    module, method = __resolve_name(maker_name)
    return getattr(importlib.import_module(module), method)

def register(alias, maker, singleton = False):
    if bindings.get(alias) is not None:
        raise KeyError
    bindings[alias] = (__import(maker), singleton)

def make(alias, *argv, **kargv):
    if not bindings.has_key(alias):
        raise 'Alias not register'
    maker, singleton = bindings[alias]
    if singleton:
        if instances.get(alias) is None:
            instances[alias] = maker(*argv, **kargv)
        return instances[alias]
    return maker(*argv, **kargv)
    
    
if __name__ == '__main__':
    pass
