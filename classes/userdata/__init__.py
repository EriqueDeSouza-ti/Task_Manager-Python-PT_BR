from dataclasses import dataclass, field
from typing import Optional



@dataclass
class User:
    id   : int
    name : str
    email: str
    password: str
    phone: Optional[int] = None
    tasks: list=field(default_factory=list)

    def __post_init__(self):
        pass