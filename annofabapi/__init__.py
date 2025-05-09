from importlib.metadata import PackageNotFoundError, version

from annofabapi.api import AnnofabApi
from annofabapi.api2 import AnnofabApi2
from annofabapi.resource import Resource, build, build_from_env, build_from_netrc
from annofabapi.wrapper import Wrapper

__all__ = [
    "AnnofabApi",
    "AnnofabApi2",
    "Resource",
    "Wrapper",
    "build",
    "build_from_env",
    "build_from_netrc",
]


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"
