"""
@author: twsswt
"""


class Bug(object):
    _count = 0

    def __init__(self, chunk):
        self.ident = Bug._count
        Bug._count += 1

        self.chunk = chunk

    @property
    def probability_failure_on_demand(self):
        return self.chunk.feature.software_system.probability_failure_on_demand

    def manifest(self, random):
        if random.random() <= self.probability_failure_on_demand:
            raise BugEncounteredException(self)

    def __repr__(self):
        return "b_%d" % self.ident


class BugEncounteredException(Exception):
    def __init__(self, bug):
        assert isinstance(bug, Bug)
        self.bug = bug

    def __str__(self):
        return "bug_encounter[%s]" % self.bug.id
