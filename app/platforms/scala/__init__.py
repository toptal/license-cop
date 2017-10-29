from app.platforms.scala.repository_matcher import ScalaRepositoryMatcher
from app.platforms.jvm.maven_package_registry import MavenPackageRegistry
from app.platform import Platform


INSTANCE = Platform('Scala', ScalaRepositoryMatcher(), MavenPackageRegistry())
