import os


def require_environment(name):
    if name in os.environ:
        value = os.environ[name].strip()
        if value:
            return value
    raise Exception(f'Required environment value {name} is not defined')
