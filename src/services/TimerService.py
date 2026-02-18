from time import perf_counter


class TimerService:
    def __init__(self):
        # Holds timer running in background
        self.timer = {}

    def start_timer(self, id: str) -> bool:
        try:
            # Holds time when timer started
            start_time = perf_counter()

            # Saving the time with given id
            self.timer[id] = start_time

            return True
        except Exception as e:
            print(e)
            return False

    def end_timer(self, id: str):
        try:
            # Holds time when timer started
            finish_time = perf_counter()

            # Saving the time with given id
            start_time = self.timer[id]

            return finish_time - start_time

        except Exception as e:
            print(e)
            return -1
