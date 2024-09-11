class EventStartDateException(Exception):
    def __init__(self, message = "The start date entered cannot be less than today"):
        self.message = message
        super().__init__(self.message)


class EventEndDateException(Exception):
    def __init__(self, message = "The end data entered cannot be less than today"):
        self.message = message
        super().__init__(self.message)


class EventNotFound(Exception):
    def __init__(self, message = "Event not found"):
        self.message = message
        super().__init__(self.message)
