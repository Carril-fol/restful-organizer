class FolderException(Exception):
    pass


class FolderNotFound(FolderException):
    def __init__(self, message="Folder not found"):
        self.message = message
        super().__init__(self.message)


class FolderNameException(FolderException):
    def __init__(self, message="Folder name cannot be blank."):
        self.message = message
        super().__init__(self.message)
