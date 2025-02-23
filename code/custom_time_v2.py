class Time:
    """
    Represents the time of day
    """

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"

    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return Time(hour, minute, second)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    def __add__(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)

    def __eq__(self, other):
        return (
            self.hour == other.hour
            and self.minute == other.minute
            and self.second == other.second
        )
