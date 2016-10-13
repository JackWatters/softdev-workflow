"""
@author: tws
"""
import sys

from sortedcontainers.sortedset import SortedSet

from .feature import Feature
from .test import Test


class SoftwareSystem(object):
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

        self.features = SortedSet(key=lambda f: f.logical_name)
        self.tests = SortedSet(key=lambda t: t.logical_name)
        self.successful_operations = []

    @property
    def chunks(self):
        chunk_sets = map(lambda f: frozenset(f.chunks), self.features)
        return reduce(lambda a, b: a.union(b), chunk_sets, SortedSet(key=lambda c: c.logical_name))

    def get_chunk(self, logical_name):
        result = filter(lambda chunk: chunk.logical_name == logical_name, self.chunks)
        if len(result) is 0:
            return None
        else:
            return result[0]

    @property
    def chunk_names(self):
        return map(lambda c: c.logical_name, self.chunks)

    @property
    def chunk_contents(self):
        return map(lambda c: c.local_content, self.chunks)

    @property
    def bugs(self):
        bug_sets = map(lambda c: frozenset(c.bugs), self.chunks)
        return reduce(lambda a, b: a.union(b), bug_sets, SortedSet(key=lambda bug: bug.ident))

    def add_feature(self, logical_name, size):
        feature = Feature(self, logical_name, size)
        self.features.add(feature)
        return feature

    def get_feature(self, logical_name):
        result = filter (lambda f: f.logical_name==logical_name, self.features)
        if len(result) is 0:
            return None
        else:
            return result[0]

    def add_test(self, logical_name, feature):
        test = Test(logical_name, feature)
        self.tests.add(test)
        return test

    def operate(self, random, limit=sys.maxint):
        current_operations = []
        self.successful_operations.append(current_operations)

        if len(self.features) == 0:
            return self.successful_operations

        while len(current_operations) < limit:
            next_feature = random.choice(self.features)
            next_feature.operate(random)
            current_operations.append(next_feature)

    @property
    def last_trace(self):
        """
        :return : the last sequence of successful operations called by operate.
        """
        last_trace_index = len(self.successful_operations) - 1

        return self.successful_operations[last_trace_index]

    @property
    def mean_operations_to_failure(self):
        total_operations = reduce(lambda x, y: x + y, map(lambda l: len(l), self.successful_operations), 0)
        if len(self.successful_operations) is 0:
            return 0
        else:
            return total_operations / len(self.successful_operations)

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
