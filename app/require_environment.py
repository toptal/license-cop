import os


def require_environment(name):
    if name in os.environ:
        value = os.environ[name].strip()
        if value:
            return value
    raise Exception('Required environment value {0} is not defined'.format(name))
