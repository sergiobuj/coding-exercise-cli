from dataclasses import dataclass, fields

from pydantic import validate_arguments


# pylint: disable=R0902
@validate_arguments
@dataclass
class LogEntry:
    """LogEntry is our dataclass for log entries in the file.

    Instances of this class will hold the information for a single entry in the log file.

    The attributes are taken from the contents of the Squid's native format for logs:
    time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type
    """

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

    def __init__(self, **kwargs):
        names = {f.name for f in fields(self)}
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)
