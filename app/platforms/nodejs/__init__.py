from app.platforms.nodejs.repository_matcher import NodejsRepositoryMatcher
from app.platforms.nodejs.package_registry import NodejsPackageRegistry
from app.platform import Platform


INSTANCE = Platform('Node.js', NodejsRepositoryMatcher(), NodejsPackageRegistry())
