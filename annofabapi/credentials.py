from dataclasses import dataclass
from typing import Dict, Protocol


class HasAuthToken(Protocol):
    @property
    def auth_token(self) -> str: ...


@dataclass(frozen=True)
class IdPass:
    user_id: str
    password: str


@dataclass(frozen=True)
class Pat(HasAuthToken):
    """Personal Access Token"""

    token: str

    @property
    def auth_token(self) -> str:
        return f"Bearer {self.token}"


@dataclass(frozen=True)
class Tokens(HasAuthToken):
    """IdPassを元にログインしたあとに取得されるトークン情報"""

    id_token: str
    access_token: str
    refresh_token: str

    @property
    def auth_token(self) -> str:
        return self.id_token

    def to_dict(self) -> Dict[str, str]:
        return {
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }

    @staticmethod
    def from_dict(d: Dict[str, str]) -> "Tokens":
        return Tokens(id_token=d["id_token"], access_token=d["access_token"], refresh_token=d["refresh_token"])
