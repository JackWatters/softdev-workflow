"""
@author twsswt
"""


class UserStory:

    def __init__(self, logical_name, size, priority):
        self.logical_name = logical_name
        self.size = size
        self.priority = priority

    def __str__(self):
        return "UserStory(%s,%d,%d)" % (self.logical_name, self.size, self.priority)

    def __repr__(self):
        return self.__str__()
