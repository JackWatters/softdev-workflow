"""
@author: tws
"""
from .feature import Feature
from .software_system import SoftwareSystem


class Developer(object):
    """
    Represents the work effort of a software developer.
    """

    def __init__(self, person_time=0):
        self.person_time = person_time
        self.completed_tasks = []

    def extend_feature(self, random, logical_name, feature):
        self._perform_task(1, Feature.extend, [feature, logical_name, random])

    def add_test(self, feature):
        self._perform_task(1, SoftwareSystem.add_test, [feature.software_system, feature])

    def debug(self, random, feature, bug):
        self._perform_task(1, Feature.debug, [feature, random, bug])

    def refactor(self, random, feature):
        self._perform_task(1, Feature.refactor, [feature, random])

    def idle(self):
        self._perform_task(1)

    def _perform_task(self, cost=0, task=None, args=None):
        """
        Private book keeping function to monitor the developer's work load.
        """
        if self.person_time - cost <= 0:
            raise DeveloperExhaustedException(self)
        else:
            self.person_time -= cost
            if task is not None:
                task(*args)
                self.completed_tasks.append([task, args])


class DeveloperExhaustedException(Exception):

    def __init__(self, developer):
        self.developer = developer
