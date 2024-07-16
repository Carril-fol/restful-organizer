class FolderException(BaseException):
    pass


class FolderNotFound(FolderException):
    def __init__(self, message = "Folder not found"):
        self.message = message
        super().__init__(self.message)