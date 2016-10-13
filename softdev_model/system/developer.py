"""
@author: tws
"""


class Developer(object):
    """
    Represents the work effort of a software developer.
    """

    def __init__(self, logical_name, person_time=0):
        self.person_time = person_time
        self.completed_tasks = []
        self.logical_name = logical_name

    def extend_feature(self, logical_name, feature, random):
        extend_method = getattr(feature, "extend")
        self._perform_task(1, extend_method, [logical_name, self, random])

    def add_test(self, software_system, logical_name, feature):
        add_test_method = getattr(software_system, "add_test")
        self._perform_task(1, add_test_method, [logical_name, feature])

    def debug(self, feature, bug, random):
        debug_method = getattr(feature, "debug")
        self._perform_task(1, debug_method, [random, bug])

    def refactor(self, feature, random):
        refactor_method = getattr(feature, "refactor")
        self._perform_task(1, refactor_method, [random])

    def update_working_copy(self, centralised_vcs_client, random):
        update_method = getattr(centralised_vcs_client, "update")
        self._perform_task(0, update_method, [centralised_vcs_client, random])

    def resolve_conflict(self, centralised_vcs_client, conflict, random):
        resolve_method = getattr(centralised_vcs_client, "resolve")
        self._perform_task(1, resolve_method, [centralised_vcs_client, conflict, random])

    def commit_changes(self, centralised_vcs_client):
        commit_method = getattr(centralised_vcs_client, "commit")
        self._perform_task(0, commit_method, [centralised_vcs_client])

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
