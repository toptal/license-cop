from app.platforms.elixir.repository_matcher import ElixirRepositoryMatcher
from app.platforms.elixir.package_registry import ElixirPackageRegistry
from app.platform import Platform


INSTANCE = Platform('Elixir', ElixirRepositoryMatcher(), ElixirPackageRegistry())
