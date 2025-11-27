from dataclasses import dataclass

@dataclass
class EPISODE:
    name: str 
    date: str 
    thumbnail: str 
    contentUrl: str 
    contentType: str 
    title: str | None
