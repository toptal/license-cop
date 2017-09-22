from app.platforms.ruby.package_registry import *
from app.platforms.ruby.repository_filter import *
from app.platform_resolver import *


PLATFORM_RESOLVERS = [
    PlatformResolver('Ruby', RubyRepositoryFilter(), RubyPackageRegistry())
]
