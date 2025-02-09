class BaseFilter:

    def to_dict(self):
        data = vars(self).copy()
        return data
