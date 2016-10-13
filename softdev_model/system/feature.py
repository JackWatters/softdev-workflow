from .chunk import Chunk
from sortedcontainers import SortedSet

"""
@author: tws
"""


class Feature(object):

    def __init__(self, software_system, logical_name, size):
        """
        Constructs a new feature specification, initially with no corresponding chunks in the system.
        """
        self._logical_name = logical_name

        self.software_system = software_system
        self.size = size

        self.chunks = SortedSet(key=lambda c: c.logical_name)

    @property
    def logical_name(self):
        return self._logical_name

    @property
    def bugs(self):
        bug_sets = map(lambda c: frozenset(c.bugs), self.chunks)
        return reduce(lambda a, b: a.union(b), bug_sets, set())

    @property
    def tests(self):
        unsorted_feature_tests = filter(lambda t: t.feature == self, frozenset(self.software_system.tests))
        return SortedSet(unsorted_feature_tests, lambda t: t.logical_name)

    @property
    def test_coverage(self):
        covered_chunks = SortedSet(
            reduce(lambda a, b: a.union(b), map(lambda t: frozenset(t.chunk_indexes), self.tests), set()))
        return float(len(covered_chunks)) / self.size

    @property
    def minimum_tests_per_chunk(self):
        return min(map(lambda c: len(c.tests), self.chunks))

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

    def extend(self, logical_name, developer, random):
        chunk = self.add_chunk(logical_name)
        chunks_to_modify = self._sample_chunks(random)
        chunks_to_modify.add(chunk)

        for chunk_to_modify in chunks_to_modify:
            chunk_to_modify.modify(developer, random)

        return chunk

    def debug(self, random, detected_bug=None):
        if detected_bug is None:
            for chunk in self.chunks:
                chunk.debug(random)

        else:
            detected_bugs = SortedSet(self.bugs & {detected_bug}, key=lambda b: b.logical_name)
            for detected_bug in detected_bugs:
                detected_bug.chunk.debug(random, detected_bug)

    def refactor(self, random):
        random.choice(self.chunks).refactor(random)

    def operate(self, my_random):
        """
        Operates a random sample of the feature's implemented chunks if the feature has been implemented.
        """
        if self.is_implemented:
            for sampled_chunk in self._sample_chunks(my_random):
                sampled_chunk.operate(my_random)

        else:
            raise InoperableFeatureException(self)

    def exercise_tests(self):
        for test in self.tests:
            test.exercise()

    def _sample_chunks(self, random):
        sample_cardinality = random.randint(0, len(self.chunks))
        sample = random.sample(self.chunks, sample_cardinality)
        return SortedSet(sample, key=lambda c: c.logical_name)

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
