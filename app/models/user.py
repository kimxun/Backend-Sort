class User:
    def __init__(self, id=None, username=None, password=None, full_name=None,
                 email=None, role=None, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
        self.created_at = created_at  

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}