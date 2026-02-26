class Episode:
    def __init__(self) -> None:
        pass

    def date(self, date: str) -> str:
        date_in_part = date.split()
        print(date_in_part)


if __name__ == "__main__":
    episode = Episode()
    episode.date("9th May Episode 43-47 2025")
