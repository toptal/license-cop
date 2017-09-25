from app.dependency import *


def parse_dependencies(data, kind):
    key = 'dependencies' if kind == DependencyKind.RUNTIME else 'devDependencies'
    if key not in data:
        return []
    return list(map(lambda i: Dependency(i, kind), data[key].keys()))
