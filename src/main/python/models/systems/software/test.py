'''
@author: tws
'''
from random import Random
from bug import BugEncounteredException
from sortedcontainers.sortedset import SortedSet

class Test(object):


    test_count = 0

    def __init__(self, feature, probability_coverage=0.5):
        self.id = Test.test_count
        Test.test_count += 1
        self.feature = feature
        self.probability_coverage = probability_coverage


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
                
            if p <= bug.pdetect:
                result.add(bug)
                
        return result


    @property
    def coverage(self):
        result = set()
        for chunk in self.feature.chunks:
            chunk_test_hash = hash(frozenset([self.id, chunk.id]))
            my_random = Random(chunk_test_hash)
            p = my_random.random()
            if p <= self.probability_coverage:
                result.add(chunk)
        return result


    def exercise (self):
        if len(self._bugs) > 0:
            bug = self._bugs[0]
            raise BugEncounteredException (bug)


    def __str__(self):
        bugs_string = ",".join(map (lambda bug : str(bug), self._bugs))
        return "t_%d[%s]" % (self.id, bugs_string)
    
    def __repr__(self):
        return "t_%d" % (self.id)



