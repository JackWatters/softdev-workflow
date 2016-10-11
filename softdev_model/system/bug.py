"""
@author: twsswt
"""


class Bug(object):

    def __init__(self, logical_name, chunk):
        self.logical_name = logical_name
        self.chunk = chunk

    @property
    def probability_failure_on_demand(self):
        return self.chunk.feature.software_system.probability_failure_on_demand

    def manifest(self, random):
        if random.random() <= self.probability_failure_on_demand:
            raise BugEncounteredException(self)

    def __repr__(self):
        return "b_%s" % str(self.logical_name)


class BugEncounteredException(Exception):
    def __init__(self, bug):
        assert isinstance(bug, Bug)
        self.bug = bug

    def __str__(self):
        return "bug_encounter[%s]" % self.bug.logical_name
