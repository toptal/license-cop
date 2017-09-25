from app.platforms.nodejs.package_registry import *
from app.platforms.nodejs.repository_matcher import *
from app.platform import *


INSTANCE = Platform('Node.js', NodejsRepositoryMatcher(), NodejsPackageRegistry())
