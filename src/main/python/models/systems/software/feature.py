from chunk import Chunk
from sortedcontainers import SortedSet
'''
@author: tws
'''
class Feature:


    _feature_count = 0


    def __init__(self, software_system, size):
        '''
        Constructs a new feature specification, initially with no corresponding chunks in the system.
        @param size: the required number of chunks for this feature to operate. 
        '''
        self.id = Feature._feature_count
        Feature._feature_count += 1
        
        self.software_system = software_system
        self.size = size
        
        self.chunks = SortedSet(key=lambda c : c.id)


    @property
    def bugs(self):
        bug_sets = map (lambda c : frozenset(c.bugs), self.chunks)
        return reduce(lambda a, b: a.union(b), bug_sets, set())


    @property
    def tests(self):
        system_tests = frozenset(self.software_system.tests)
        return filter(lambda t : t.feature == self, system_tests)
    
    
    @property
    def test_coverage(self):
        chunk_sets = map(lambda t : frozenset(t.coverage), self.tests)
        return reduce(lambda a, b : a.union(b), chunk_sets, set())


    @property
    def is_implemented(self):
        return len(self.chunks) >= self.size

    
    def extend(self, random):

        chunk = Chunk(self)
        self.chunks.add(chunk)
        chunks_to_modify = self._sample_chunks(random)
        chunks_to_modify.add(chunk)##

        for chunk_to_modify in chunks_to_modify:
            chunk_to_modify.modify(random)
        
        return chunk


    def debug(self, random, detected_bug=None):

        if detected_bug == None:
            for chunk in self.chunks:
                chunk.debug(random)

        else:
            detected_bugs = SortedSet(self.bugs & set ([detected_bug]), key=lambda b : b.id)
            for detected_bug in detected_bugs:
                detected_bug.chunk.debug(random, detected_bug)


    def refactor(self, random):
        random.choice(self.chunks).refactor(random)


    def operate(self, my_random):
        '''
        Operates a random sample of the feature's implemented chunks if the feature has been implemented.
        '''
        if self.is_implemented:
            for sampled_chunk in self._sample_chunks(my_random):
                sampled_chunk.operate(my_random)

        else:
            raise InoperableFeatureException(self)


    def _sample_chunks(self, random):
        sample_cardinality = random.randint(0, len(self.chunks))
        sample = random.sample (self.chunks, sample_cardinality)
        return SortedSet(sample, key=lambda c : c.id)


    def __str__(self):

        chunk_strings = map (lambda chunk : str(chunk), self.chunks)
        return "f_%d[%s]" % (self.id, ",".join(chunk_strings))


    def __repr__(self):
        return "f_%d" % (self.id)


class InoperableFeatureException(Exception):


    def __init__(self, feature):
        self.feature = feature