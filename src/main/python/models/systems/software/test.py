'''
@author: tws
'''
from _random import Random
from bug import BugEncounteredException

class Test(object):


    test_count = 0

    def __init__(self, feature):
        self.id = Test.test_count
        Test.test_count += 1
        self.feature = feature


    @property
    def _bugs(self):
        result = set()

        random = Random()
        for bug in self.feature.bugs:
            bug_test_hash = hash(frozenset([self.id, bug.id]))
            random.seed(bug_test_hash)
            p = random.random()
            if p <= bug.pfd:
                result.add(bug)
                
        return result


    def exercise (self):
        if len(self._bugs) > 0:
            bug = next(iter(self._bugs))
            raise BugEncounteredException (bug)


    def __str__(self):
        bugs_string = ",".join(map (lambda bug : str(bug), self._bugs))
        return "t_%d[%s]" % (self.id, bugs_string)



