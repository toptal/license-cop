from app.platforms.python.repository_matcher import PythonRepositoryMatcher
from app.platforms.python.package_registry import PythonPackageRegistry
from app.platform import Platform


INSTANCE = Platform('Python', PythonRepositoryMatcher(), PythonPackageRegistry())
