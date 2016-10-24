from random import Random
from sortedcontainers import SortedSet


class SystemRandom(Random):
    """
    Extends the random class with a higher level API for operations that require random behaviour.
    """
    def __int__(self, *args):
        Random.__init__(self, *args)

    def sample_chunks(self, chunks):
        sample_cardinality = self.randint(0, len(chunks))
        sample = self.sample(chunks, sample_cardinality)
        return SortedSet(sample, key=lambda c: c.fully_qualified_name)

    def choose_chunk(self, chunks):
        return self.choice(chunks)

    def dependency_should_be_added(self, threshold):
        return self.random() <= threshold

    def dependency_should_be_removed(self, chunk, dependency):
        p = self.random()
        if (dependency.feature == chunk.feature and p <= chunk.probability_lose_feature_dependency) or\
                p < chunk.probability_lose_system_dependency:
            return True

    def known_bug_should_be_removed(self, chunk):
        return self.random() <= chunk.probability_debug_known

    def unknown_bug_should_be_removed(self, chunk):
        return self.random() <= chunk.probability_debug_unknown

    def create_local_content(self):
        return self.randint(0, 100)

    def a_bug_should_be_inserted(self, chunk):
        return self.random() <= chunk.probability_new_bug

    def bug_manifests_itself(self, bug):
        return self.random() <= bug.probability_failure_on_demand
