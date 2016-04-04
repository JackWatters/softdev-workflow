'''
@author: tws
'''
from random import Random
from bug import BugEncounteredException
from sortedcontainers.sortedset import SortedSet


class Test(object):
    test_count = 0

    def __init__(self, feature, ):
        self.id = Test.test_count
        Test.test_count += 1
        self.feature = feature

    @property
    def _covered_bugs(self):
        covered_bug_sets = map(lambda c: frozenset(c.bugs), self.coverage)
        return reduce(lambda a, b: a.union(b), covered_bug_sets, set())

    @property
    def _bugs(self):
        result = SortedSet(key=lambda b: b.id)

        for bug in self._covered_bugs:
            my_random = Random()
            bug_test_hash = hash(frozenset([self.id, bug.id]))
            my_random.seed(bug_test_hash)
            p = my_random.random()

            if p <= self.probability_detect:
                result.add(bug)

        return result

    @property
    def probability_detect(self):
        return self.feature.software_system.probabilities['detection']

    @property
    def probability_chunk_covered(self):
        return self.feature.software_system.probabilities['coverage']

    @property
    def coverage(self):
        result = set()
        for chunk in self.feature.chunks:
            chunk_test_hash = hash(frozenset([self.id, chunk.id]))
            rand = Random(chunk_test_hash)
            if rand.random() <= self.probability_chunk_covered:
                result.add(chunk)
        return result

    def exercise(self):
        if len(self._bugs) > 0:
            bug = self._bugs[0]
            raise BugEncounteredException(bug)

    def __str__(self):
        bugs_string = ",".join(map(lambda bug: str(bug), self._bugs))
        return "t_%d[%s]" % (self.id, bugs_string)

    def __repr__(self):
        return "t_%d" % (self.id)
