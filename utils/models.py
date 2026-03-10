from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PersonResult:
    source: str
    found: bool
    data: dict
    errors: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
