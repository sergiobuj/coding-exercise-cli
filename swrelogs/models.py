from dataclasses import dataclass


# pylint: disable=R0902
@dataclass
class LogEntry:
    """time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type"""

    timestamp: float = 0
    elapsed: int = 0
    remotehost: str = ""
    status: str = ""
    bytes: int = 0
    method: str = ""
    url: str = ""
    user: str = ""
    peer: str = ""
    type: str = ""
