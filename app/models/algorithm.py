class Algorithm:
    def __init__(self, id=None, name=None, code=None, description=None,
                 time_complexity=None, space_complexity=None, category_id=None, slug=None):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.time_complexity = time_complexity
        self.space_complexity = space_complexity
        self.category_id = category_id  
        self.slug = slug

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}