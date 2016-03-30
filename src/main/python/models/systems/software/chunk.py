'''
@author: tws
'''
from bug import Bug

class Chunk:

    chunk_count = 0

    def __init__(
        self,
        feature,

        probability_gain_feature_dependency = 0.1,
        probability_gain_system_dependency = 0.05,
        probability_lose_feature_dependency = 0.05,
        probability_lose_system_dependency = 0.05,

        probability_new_bug = 0.5,
        probability_debug_known=0.9,
        probability_debug_unknown=0.01
    ):
        self.id = Chunk.chunk_count
        Chunk.chunk_count += 1;
        
        self.feature = feature

        self.probability_gain_feature_dependency = probability_gain_feature_dependency
        self.probability_gain_system_dependency = probability_gain_system_dependency

        self.probability_lose_feature_dependency = probability_lose_feature_dependency
        self.probability_lose_system_dependency = probability_lose_system_dependency

        self.probability_new_bug = probability_new_bug
        self.probability_debug_known=probability_debug_known
        self.probability_debug_unknown=probability_debug_unknown
        
        self.dependencies = set()
        self.bugs = set()
        

    def modify (self, random):
        feature_chunks = self.feature.chunks.difference([self])
        system_chunks = self.feature.software_system.chunks.difference(self.feature.chunks)

        self._add_dependencies(random, system_chunks, self.probability_gain_system_dependency)
        self._add_dependencies(random, feature_chunks, self.probability_gain_feature_dependency)
                        
        self._insert_bugs(random)


    def _add_dependencies(self, random, candidate_chunks, probability):
        for candidate in candidate_chunks:
            if random.random() <= probability:
                self.dependencies.add(candidate)


    def _insert_bugs(self, random):
        while random.random() <= self.probability_new_bug:
            self.bugs.add(Bug(self))


    def refactor (self, random):
        to_remove = set()
        for existing_chunk in self.dependencies:
            p = random.random()
            if existing_chunk.feature == self.feature and p <= self.probability_lose_feature_dependency:
                to_remove.add(existing_chunk)
            elif p < self.probability_lose_system_dependency:
                to_remove.add(existing_chunk)
                
        self.dependencies.difference_update(to_remove)


    def debug (self, random, bug=None):
        if len(self.bugs) == 0:
            return
        
        elif not (bug == None) and random.random() <= self.probability_debug_known:
            self.bugs.remove(bug)
        else:
            bug = random.choice([self.bugs])
            if random.random() <= self.probability_debug_unknown:
                self.bugs.remove(bug)


    def operate(self, random):
        for bug in self.bugs_in_dependencies.union(self.bugs):
            bug.manifest(random)


    @property
    def bugs_in_dependencies(self):
        chunk_bug_set = frozenset(map(lambda chunk : frozenset(chunk.bugs), self.dependencies))
        return reduce(lambda bugs_a, bugs_b: bugs_a.union(bugs_b), chunk_bug_set, set())


    def __str__(self):
        
        dependencies = ", ".join(map (lambda dependency : repr(dependency), self.dependencies))
        bugs = ", ".join(map (lambda bug : str(bug), self.bugs))
                    
        return "c_%d:[%s]->[%s]" % (self.id, bugs, dependencies);
    
    
    def __repr__(self):
        return "c%d" % self.id