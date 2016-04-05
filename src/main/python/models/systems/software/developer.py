"""
@author: tws
"""
from models.systems.software.softwaresystem import SoftwareSystem

class Developer(object):
    """
    Represents the work effort of a software developer.
    """

    def __init__(self, person_time):
        self.person_time = person_time

    def extend_feature(self, random, feature):
        self.person_time -= 1
        feature.extend(random)

    def debug(self, random, feature, bug):
        self.person_time -=1
        feature.debug(random, bug)

    def add_test(self, feature):
        self._perform_task(SoftwareSystem.add_test, [feature.software_system, feature], 1)

    def refactor(self, random, feature):
        self.person_time -= 1
        feature.refactor(random)

    def _perform_task (self, task, args, cost):
        """
        Private book keeping function to monitor the developer's work load.
        """
        if self.person_time - cost <= 0:
            raise DeveloperExhaustedException(self)
        else:
            self.person_time -= cost
            task(*args)


class DeveloperExhaustedException(Exception):

    def __init__(self, developer):
        self.developer = developer
