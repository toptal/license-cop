from app.platforms.ruby.repository_matcher import RubyRepositoryMatcher
from app.platforms.ruby.package_registry import RubyPackageRegistry
from app.platform import Platform


INSTANCE = Platform('Ruby', RubyRepositoryMatcher(), RubyPackageRegistry())
