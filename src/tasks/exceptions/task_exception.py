class TaskException(Exception):
    pass


class TaskNotExists(TaskException):
    def __init__(self, message = "Task not exists."):
        self.message = message
        super().__init__(self.message)


class StatusNotValid(TaskException):
    def __init__(self, message = "Status introduced not valid."):
        self.message = message
        super().__init__(self.message)