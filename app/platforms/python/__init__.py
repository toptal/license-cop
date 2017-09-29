from app.platforms.python.package_registry import *
from app.platforms.python.repository_matcher import *
from app.platform import *


INSTANCE = Platform('Python', PythonRepositoryMatcher(), PythonPackageRegistry())
