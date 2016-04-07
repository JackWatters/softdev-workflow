"""
@author: tws
"""
from bug import Bug
from sortedcontainers import SortedSet


class Chunk:
    """
    Represents a chunk of code providing some useful functionality in the system.
    """

    _count = 0

    def __init__(self, feature):
        self.id = Chunk._count
        Chunk._count += 1;

        self.feature = feature

        self.dependencies = SortedSet(key=lambda d: d.id)
        self.bugs = SortedSet(key=lambda b: b.id)

    @property
    def probability_gain_feature_dependency(self):
        return self.feature.software_system.probability_gain_feature_dependency

    @property
    def probability_lose_feature_dependency(self):
        return self.feature.software_system.probability_lose_feature_dependency

    @property
    def probability_gain_system_dependency(self):
        return self.feature.software_system.probability_gain_system_dependency

    @property
    def probability_lose_system_dependency(self):
        return self.feature.software_system.probability_lose_system_dependency

    @property
    def probability_new_bug(self):
        return self.feature.software_system.probability_new_bug

    @property
    def probability_debug_known(self):
        return self.feature.software_system.probability_debug_known

    @property
    def probability_debug_unknown(self):
        return self.feature.software_system.probability_debug_unknown

    def modify(self, random):
        feature_chunks = self.feature.chunks - set([self])
        system_chunks = set(self.feature.software_system.chunks.difference(self.feature.chunks))
        self._add_dependencies(random, system_chunks, self.probability_gain_system_dependency)
        self._add_dependencies(random, feature_chunks, self.probability_gain_feature_dependency)

        self._insert_bugs(random)

    def _add_dependencies(self, my_random, candidate_chunks, probability):
        for candidate in SortedSet(candidate_chunks, key=lambda c: c.id):
            p = my_random.random()
            if p <= probability:
                self.dependencies.add(candidate)

    def _insert_bugs(self, random):
        while random.random() <= self.probability_new_bug:
            self.bugs.add(Bug(self))

    def refactor(self, random):
        to_remove = set()
        for existing_chunk in self.dependencies:
            p = random.random()
            if existing_chunk.feature == self.feature and p <= self.probability_lose_feature_dependency:
                to_remove.add(existing_chunk)
            elif p < self.probability_lose_system_dependency:
                to_remove.add(existing_chunk)

        self.dependencies.difference_update(to_remove)

    def debug(self, random, bug=None):

        if len(self.bugs) == 0:
            return

        elif not (bug is None) and random.random() <= self.probability_debug_known:
            self.bugs.remove(bug)
        else:
            bug = random.choice(self.bugs)
            if random.random() <= self.probability_debug_unknown:
                self.bugs.remove(bug)

    def operate(self, random):
        for bug in self.bugs_in_dependencies.union(self.bugs):
            bug.manifest(random)

    @property
    def bugs_in_dependencies(self):
        chunk_bug_set = frozenset(map(lambda chunk: frozenset(chunk.bugs), self.dependencies))
        return reduce(lambda bugs_a, bugs_b: bugs_a.union(bugs_b), chunk_bug_set, set())

    def __str__(self):
        string_repr_set = lambda iterable: ",".join(map(lambda e: repr(e), iterable))

        feature_dependencies = string_repr_set(filter(lambda c: c.feature == self.feature, self.dependencies))
        system_dependencies = string_repr_set(filter(lambda c: c.feature != self.feature, self.dependencies))

        bugs = ", ".join(map(lambda bug: str(bug), self.bugs))

        return "c_%d:[%s]->(in[%s],ex[%s])" % (self.id, bugs, feature_dependencies, system_dependencies)

    def __repr__(self):
        return "c%d" % self.id
