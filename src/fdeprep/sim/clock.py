"""A virtual clock, so retry and backoff code runs instantly."""


class VirtualClock:
    def __init__(self, start: float = 0.0) -> None:
        self.now = start
        self.slept = 0.0

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("cannot sleep a negative time")
        self.now += seconds
        self.slept += seconds
