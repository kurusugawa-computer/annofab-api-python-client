from importlib.metadata import PackageNotFoundError, version
from annofabapi.api import AnnofabApi
from annofabapi.api2 import AnnofabApi2
from annofabapi.wrapper import Wrapper
from annofabapi.resource import build, build_from_netrc, build_from_env, Resource


__all__ = [
    "AnnofabApi",
    "AnnofabApi2",
    "Wrapper",
    "build",
    "build_from_netrc",
    "build_from_env",
    "Resource",
]


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"
 