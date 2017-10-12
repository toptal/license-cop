from app.platforms.scala.repository_matcher import ScalaRepositoryMatcher
from app.platforms.jvm.maven2_package_registry import Maven2PackageRegistry
from app.platform import Platform


INSTANCE = Platform('Scala', ScalaRepositoryMatcher(), Maven2PackageRegistry())
