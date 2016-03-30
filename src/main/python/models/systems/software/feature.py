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


    def extend(self, random):

        chunk = Chunk(self, random)
        self.chunks.add(chunk)

        chunks_to_modify = Set(random.sample(self.chunks, random.randint(0,len(self.chunks))))
        chunks_to_modify.add(chunk)
        for chunk_to_modify in chunks_to_modify:
            chunk_to_modify.modify(random)

        return chunk


    def debug(self, random, detected_bug=None):

        if detected_bug == None:
            for chunk in self.chunks:
                chunk.debug(random)

        else:
            detected_bugs = self.bugs.intersection([detected_bug])
            for detected_bug in detected_bugs:
                detected_bug.chunk.debug(random, detected_bug)


    def is_implemented(self):
        return len(self.chunks) >= self.size


    def operate(self, random):
        '''
        Operates a random sample of the feature's implemented chunks if the feature has been implemented.
        '''
        if self.is_implemented():
            sampled_chunks = \
                random.sample (self.chunks, random.randint(0, len(self.chunks)))
            
            for sampled_chunk in sampled_chunks:
                sampled_chunk.operate(random)

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