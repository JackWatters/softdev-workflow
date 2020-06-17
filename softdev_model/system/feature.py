"""
@author: tws
"""

from functools import reduce


from .chunk import Chunk
from .test import Test
from sortedcontainers import SortedSet


class Feature(object):

    def __init__(self, software_system, logical_name, size):
        """
        Constructs a new feature specification, initially with no corresponding chunks in the system.
        """
        self._logical_name = logical_name

        self.software_system = software_system
        self.size = size

        self.chunks = SortedSet(key=lambda c: c.logical_name)
        self.tests = SortedSet(key=lambda t: t.logical_name)

    @property
    def logical_name(self):
        return self._logical_name

    @property
    def bugs(self):
        bug_sets = map(lambda c: frozenset(c.bugs), self.chunks)
        return reduce(lambda a, b: a.union(b), bug_sets, SortedSet(key=lambda b: b.fully_qualified_name))

    @property
    def test_coverage(self):
        covered_chunks = SortedSet(
            reduce(lambda a, b: a.union(b), map(lambda t: frozenset(t.chunk_indexes), self.tests), set()))
        return float(len(covered_chunks)) / self.size

    @property
    def tests_per_chunk_ratio(self):

        return 1.0*len(self.tests) / self.size

    @property
    def dependencies(self):
        all_dependencies = reduce(lambda a, b: a.union(b), map(lambda c: frozenset(c.dependencies), self.chunks), set())
        external_dependencies = filter(lambda c: c.feature != self, all_dependencies)
        return SortedSet(external_dependencies, lambda c: c.logical_name)

    @property
    def is_implemented(self):
        return len(self.chunks) >= self.size

    def add_chunk(self, logical_name, local_content=None):
        chunk = Chunk(logical_name, self, local_content)
        self.chunks.add(chunk)
        return chunk

    def extend(self, logical_name, random):
        chunk = self.add_chunk(logical_name)
        chunks_to_modify = random.sample_chunks(self.chunks)
        chunks_to_modify.add(chunk)

        for chunk_to_modify in chunks_to_modify:
            chunk_to_modify.modify(random)

        return chunk

    def debug(self, random, detected_bug=None):
        if detected_bug is None:
            for chunk in self.chunks:
                chunk.debug(random)

        else:
            detected_bugs = SortedSet(self.bugs & {detected_bug}, key=lambda b: b.fully_qualified_name)
            for detected_bug in detected_bugs:
                detected_bug.chunk.debug(random, detected_bug)

    def refactor(self, random):
        random.choose_chunk(self.chunks).refactor(random)

    def add_test(self, logical_name):
        test = Test(logical_name, self)
        self.tests.add(test)
        return test

    def operate(self, random):
        """
        Operates a random sample of the feature's implemented chunks if the feature has been implemented.
        """
        if self.is_implemented:
            for sampled_chunk in random.sample_chunks(self.chunks):
                sampled_chunk.operate(random)

        else:
            raise InoperableFeatureException(self)

    def exercise_tests(self):
        for test in self.tests:
            test.exercise()

    def __str__(self):
        chunk_strings = map(lambda chunk: str(chunk), self.chunks)
        return "f_%d[%s]" % (self._logical_name, ",".join(chunk_strings))

    def __repr__(self):
        return "f_%s" % self._logical_name


class InoperableFeatureException(Exception):
    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return "incomplete_feature[%s]" % self.feature.ident
