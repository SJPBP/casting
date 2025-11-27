from dataclasses import dataclass

@dataclass
class EPISODE:
    date: str 
    thumbnail: str 
    contentUrl: str 
    title: str | None
    contentType: str | None = None
