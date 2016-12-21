import enum
from typing import List, Callable, Dict, Tuple

from webhookforwarder.request import Request


class IconType(enum.Enum):
    url = 1,
    emoji = 2


class Config:
    def __init__(self, token: str, team_id: str, channel_id: str, forward_to: str, user_ids: List[str] = None,
                 icon_dict: Dict[str, Tuple[IconType, str]] = None,
                 forward_func: Callable[[Request], str] = lambda r: r.text,
                 response_func: Callable[[Request], str] = None,
                 response_name_func: Callable[[Request], str] = None):
        self.token = token
        self.team_id = team_id
        self.channel_id = channel_id
        self.forward_to = forward_to
        if user_ids is None:
            self.user_ids = []
        else:
            self.user_ids = user_ids
        if icon_dict is None:
            self.icon_dict = {}
        else:
            self.icon_dict = icon_dict
        self.response_func = response_func
        self.response_name_func = response_name_func
        self.forward_func = forward_func

    @property
    def identity(self) -> str:
        return self.team_id + '/' + self.channel_id
