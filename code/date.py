class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    def __eq__(self, value):
        return (
            self.year == value.year
            and self.month == value.month
            and self.day == value.day
        )

    def to_tuple(self):
        return (self.year, self.month, self.day)

    def __lt__(self, value):
        return self.to_tuple() < value.to_tuple()

    def __le__(self, value):
        return self.to_tuple() <= value.to_tuple()
