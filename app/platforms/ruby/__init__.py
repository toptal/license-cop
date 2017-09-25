from app.platforms.ruby.package_registry import *
from app.platforms.ruby.repository_matcher import *
from app.platform import *


INSTANCE = Platform('Ruby', RubyRepositoryMatcher(), RubyPackageRegistry())
