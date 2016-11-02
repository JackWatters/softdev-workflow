"""
@author: tws
"""

from .bug import Bug
from sortedcontainers import SortedSet


class Chunk(object):
    """
    Represents a chunk of code providing some useful functionality in the system.
    """

    def __init__(self, logical_name, feature, local_content=None):
        self.logical_name = logical_name

        self.feature = feature

        self.local_content = local_content

        self.dependencies = SortedSet(key=lambda d: d.logical_name)
        self.bugs = SortedSet(key=lambda b: b.logical_name)

        self.bug_count = 0

    def __eq__(self, other):
        if self.local_content != other.local_content:
            return False
        elif self.bugs_logical_names != other.bugs_logical_names:
            return False
        elif self.dependency_logical_names != other.dependency_logical_names:
            return False
        else:
            return True

    def __ne__(self, other):
        return not(self.__eq__(other))

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

    @property
    def dependency_logical_names(self):
        return map(lambda d: d.logical_name, self.dependencies)

    @property
    def bugs_logical_names(self):
        return map(lambda b: b.logical_name, self.bugs)

    @property
    def bugs_in_dependencies(self):
        chunk_bug_set = frozenset(map(lambda chunk: frozenset(chunk.bugs), self.dependencies))
        return reduce(lambda bugs_a, bugs_b: bugs_a.union(bugs_b), chunk_bug_set, set())

    @property
    def tests(self):
        return filter(lambda t: self in t.chunks, self.feature.tests)

    def modify(self, random):
        feature_chunks = self.feature.chunks - {self}
        system_chunks = set(self.feature.software_system.chunks.difference(self.feature.chunks))
        self._add_dependencies(random, system_chunks, self.probability_gain_system_dependency)
        self._add_dependencies(random, feature_chunks, self.probability_gain_feature_dependency)

        self.local_content = random.create_local_content()

        self._insert_bugs(random)

    def merge(self, source_chunk, random):
        for dependency in source_chunk.dependencies:
            working_copy_dependency = self.feature.software_system.get_chunk(dependency.fully_qualified_name)
            self.dependencies.add(working_copy_dependency)

        self.modify(random)

    def overwrite_with(self, source_chunk):

        self.local_content = source_chunk.local_content

        self.bugs.clear()
        for old_bug in source_chunk.bugs:
            new_bug = self.get_bug(old_bug.logical_name)
            if new_bug is None:
                self.add_bug(old_bug.logical_name)

        self.dependencies.clear()
        for dependency in source_chunk.dependencies:
            new_dependency = self.feature.software_system.get_chunk(dependency.fully_qualified_name)
            self.dependencies.add(new_dependency)

    def _add_dependencies(self, random, candidate_chunks, threshold):
        for candidate in SortedSet(candidate_chunks, key=lambda c: c.logical_name):
            if random.dependency_should_be_added(threshold):
                self.add_dependency(candidate)

    def add_dependency(self, candidate):
        self.dependencies.add(candidate)

    def _insert_bugs(self, random):
        while random.a_bug_should_be_inserted(self):
            self.add_bug(self.bug_count)
            self.bug_count += 1

    def add_bug(self, logical_name):
        self.bugs.add(Bug(logical_name, self))

    def get_bug(self, logical_name):
        result = filter(lambda bug: bug.logical_name == logical_name, self.bugs)
        if len(result) is 0:
            return None
        else:
            return result[0]

    def refactor(self, random):
        to_remove = set()
        for dependency in self.dependencies:

            if random.dependency_should_be_removed(self, dependency):
                to_remove.add(dependency)

        self.dependencies.difference_update(to_remove)

    def debug(self, random, bug=None):

        if len(self.bugs) == 0:
            return False

        if bug is None or bug not in self.bugs:
            if random.unknown_bug_should_be_removed(self):
                bug = random.choose_bug(self)
                self.bugs.remove(bug)
        elif random.known_bug_should_be_removed(self):
            self.bugs.remove(bug)

    def operate(self, random):
        for bug in self.bugs_in_dependencies.union(self.bugs):
            bug.manifest(random)

    def __str__(self):
        def string_repr_set(iterable):
            return ",".join(map(lambda e: repr(e), iterable))

        feature_dependencies = string_repr_set(filter(lambda c: c.feature == self.feature, self.dependencies))
        system_dependencies = string_repr_set(filter(lambda c: c.feature != self.feature, self.dependencies))

        bugs = ", ".join(map(lambda bug: str(bug), self.bugs))

        return "c_%s:[%s]:[%s]->(in[%s],ex[%s])" % \
               (str(self.logical_name), self.local_content, bugs, feature_dependencies, system_dependencies)

    @property
    def fully_qualified_name(self):
        return "%s.%s" % (str(self.feature.logical_name), str(self.logical_name))

    def __repr__(self):
        return "c%s" % str(self.fully_qualified_name)
