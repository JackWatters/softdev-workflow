"""
@author: twsswt
"""
from random import Random

from sortedcontainers.sortedset import SortedSet

from .bug import BugEncounteredException


class Test(object):
    _count = 0

    def __init__(self, feature):
        self.id = Test._count
        Test._count += 1

        self.feature = feature

    @property
    def effectiveness(self):
        return self.feature.software_system.test_effectiveness

    @property
    def efficiency(self):
        return self.feature.software_system.test_efficiency

    @property
    def chunks(self):
        return map(lambda i: self.feature.chunks[i], filter(lambda i: i < len(self.feature.chunks), self.chunk_indexes))

    @property
    def _bugs(self):
        covered_bugs = reduce(lambda a, b: a.union(b), map(lambda c: frozenset(c.bugs), self.chunks), set())

        result = SortedSet(key=lambda b: b.id)

        for bug in SortedSet(covered_bugs, key=lambda b: b.id):
            rand = Random()
            bug_test_hash = hash((self.id, bug.id))
            rand.seed(bug_test_hash)
            p = rand.random()
            if p <= self.effectiveness:
                result.add(bug)

        return result

    @property
    def chunk_indexes(self):
        """
        The indexes to chunks in the sorted set of chunks of this tests's parent feature that this tests touches.
        """
        shuffled_indexes = range(0, self.feature.size)
        shuffler = Random(self.id)
        shuffler.shuffle(shuffled_indexes)

        result = SortedSet()
        rand = Random(self.id)

        for chunk_index in shuffled_indexes:
            p = rand.random()

            if p <= self.efficiency ** (len(result)):
                result.add(chunk_index)

        return result

    def exercise(self):
        if len(self._bugs) > 0:
            bug = self._bugs[0]
            raise BugEncounteredException(bug)

    def __str__(self):
        bugs_string = ",".join(map(lambda bug: str(bug), self._bugs))
        return "t_%d[%s]" % (self.id, bugs_string)

    def __repr__(self):
        return "t_%d" % self.id
