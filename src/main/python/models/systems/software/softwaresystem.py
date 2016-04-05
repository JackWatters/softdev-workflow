'''
@author: tws
'''
import sys
from feature import Feature
from test import Test
from sortedcontainers.sortedset import SortedSet

class SoftwareSystem:
    def __init__(self,
                 probability_gain_feature_dependency=0.5,
                 probability_lose_feature_dependency=0.25,
                 probability_gain_system_dependency=0.1,
                 probability_lose_system_dependency=0.25,
                 probability_new_bug=0.5,
                 probability_debug_known=0.9,
                 probability_debug_unknown=0.01,
                 probability_failure_on_demand=0.01,
                 test_effectiveness=0.5,
                 test_efficiency=0.5
                 ):

        self.probability_gain_feature_dependency = probability_gain_feature_dependency
        self.probability_lose_feature_dependency = probability_lose_feature_dependency
        self.probability_gain_system_dependency = probability_gain_system_dependency
        self.probability_lose_system_dependency = probability_lose_system_dependency
        self.probability_new_bug = probability_new_bug
        self.probability_debug_known = probability_debug_known
        self.probability_debug_unknown = probability_debug_unknown
        self.probability_failure_on_demand = probability_failure_on_demand
        self.test_effectiveness = test_effectiveness
        self.test_efficiency = test_efficiency

        self.features = SortedSet(key=lambda f: f.id)
        self.tests = SortedSet(key=lambda t: t.id)
        self.successful_operations = []
        self.last_exception = None

    @property
    def chunks(self):
        chunk_sets = map(lambda f: frozenset(f.chunks), self.features)
        return reduce(lambda a, b: a.union(b), chunk_sets, set())

    @property
    def bugs(self):
        bug_sets = map(lambda c: frozenset(c.bugs), self.chunks)
        return reduce(lambda a, b: a.union(b), bug_sets, set())

    def add_feature(self, size):
        feature = Feature(self, size)
        self.features.add(feature)
        return feature

    def add_test(self, feature):
        test = Test(feature)
        self.tests.add(test)
        return test

    def operate(self, random, limit=sys.maxint):
        self.successful_operations = []

        if len(self.features) == 0:
            return self.successful_operations

        while len(self.successful_operations) < limit:
            next_feature = random.choice(self.features)
            next_feature.operate(random)
            self.successful_operations.append(next_feature)

    def __str__(self):
        result = []

        for feature in self.features:
            result.append(" ")
            result.append(repr(feature))
            result.append("[\n")

            for chunk in feature.chunks:
                result.append("  ")
                result.append(str(chunk))
                result.append("\n")
            result.append("]\n")

        result.append("[\n")
        for test in self.tests:
            result.append(" ")
            result.append(str(test))
            result.append("\n")

        result.append("]")

        return "".join(result)
