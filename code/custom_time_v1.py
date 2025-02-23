import copy


class Time:
    """
    Represent a time of day
    """


def print_time(time):
    s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def increment_time(time, hours, minutes, seconds):
    time.hour += hours
    time.minute += minutes
    time.second += seconds

    carry, time.second = divmod(time.second, 60)
    carry, time.minute = divmod(time.minute + carry, 60)
    carry, time.hour = divmod(time.hour + carry, 60)


def add_time(time, hours, minutes, seconds):
    total = copy.copy(time)
    increment_time(total, hours, minutes, seconds)
    return total
