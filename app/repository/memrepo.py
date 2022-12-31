from app.domain.user import User


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self):
        return [User.from_dict(i) for i in self.data]