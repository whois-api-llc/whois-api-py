class BaseModel:
    def __init__(self):
        pass

    def __str__(self):
        result = {}
        for k, v in self.__dict__.items():
            result[k] = str(v)
        return str(result)

    def __eq__(self, other):
        is_equal = isinstance(other, self.__class__)
        for k, v in self.__dict__.values():
            is_equal = is_equal and (other.__dict__.get(k) == v)

        return is_equal

    def __getitem__(self, item):
        if type(item) is str and item in self.__dict__:
            return self.__dict__[item]
        raise KeyError("Invalid key: {}".format(item))
