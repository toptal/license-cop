from app.platforms.ios.repository_matcher import IosRepositoryMatcher
from app.platforms.ios.package_registry import IosPackageRegistry
from app.platform import Platform


INSTANCE = Platform('iOS', IosRepositoryMatcher(), IosPackageRegistry())
