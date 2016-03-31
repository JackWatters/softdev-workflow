from chunk import Chunk
from sets import Set
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
        
        self.chunks = Set()


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

        chunks_to_modify = set(self.sample_chunks(random))
        chunks_to_modify.add(chunk)
##
        for chunk_to_modify in sorted(self.chunks, key=lambda c : c.id):
            chunk_to_modify.modify(random)
        
        return chunk


    def debug(self, random, detected_bug=None):

        if detected_bug == None:
            for chunk in sorted(self.chunks, key=lambda c : c.id):
                chunk.debug(random)

        else:
            detected_bugs = self.bugs.intersection([detected_bug])
            for detected_bug in sorted(detected_bugs, key=lambda b : b.id):
                detected_bug.chunk.debug(random, detected_bug)


    def refactor(self, random):
        chunk = random.choice(sorted(self.chunks, key=lambda c : c.id))
        chunk.refactor(random)


    def sample_chunks(self, random):
        sample_cardinality = random.randint(0, len(self.chunks))
        return random.sample (sorted(self.chunks, key=lambda c: c.id), sample_cardinality)


    def operate(self, my_random):
        '''
        Operates a random sample of the feature's implemented chunks if the feature has been implemented.
        '''
        if self.is_implemented:
            for sampled_chunk in sorted(self.sample_chunks(my_random), key=lambda c: c.id):
                sampled_chunk.operate(my_random)

        else:
            raise InoperableFeatureException(self)


    def __str__(self):

        chunk_strings = map (lambda chunk : str(chunk), self.chunks)
        return "f_%d[%s]" % (self.id, ",".join(chunk_strings))


    def __repr__(self):
        return "f_%d" % (self.id)


class InoperableFeatureException(Exception):


    def __init__(self, feature):
        self.feature = feature