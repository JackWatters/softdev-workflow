"""
@author: tws
"""
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.feature import Feature


class Developer(object):
    """
    Represents the work effort of a software developer.
    """

    def __init__(self, person_time=0):
        self.person_time = person_time
        self.completed_tasks = []

    def extend_feature(self, random, feature):
        self._perform_task(Feature.extend, [feature, random], 1)

    def debug(self, random, feature, bug):
        self._perform_task(Feature.debug, [feature, random, bug], 1)

    def add_test(self, feature):
        self._perform_task(SoftwareSystem.add_test, [feature.software_system, feature], 1)

    def refactor(self, random, feature):
        self._perform_task(Feature.refactor, [feature, random], 1)

    def _perform_task(self, task, args, cost):
        """
        Private book keeping function to monitor the developer's work load.
        """
        if self.person_time - cost <= 0:
            raise DeveloperExhaustedException(self)
        else:
            self.person_time -= cost
            task(*args)
            self.completed_tasks.append([task, args])


class DeveloperExhaustedException(Exception):

    def __init__(self, developer):
        self.developer = developer
