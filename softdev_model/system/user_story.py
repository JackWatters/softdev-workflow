"""
@author twsswt
"""


class UserStory:

    def __init__(self, logical_name, size):
        self.logical_name = logical_name
        self.size = size

    def __str__(self):
        return "UserStory(%s,%d)" % (self.logical_name, self.size)

    def __repr__(self):
        return self.__str__()
