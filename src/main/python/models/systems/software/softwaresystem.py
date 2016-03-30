'''
@author: tws
'''
import sys
from feature import Feature
from test import Test
from bug import BugEncounteredException
from sets import Set
from models.systems.software.feature import InoperableFeatureException

class SoftwareSystem:


    def __init__(self):
        self.failed = False
        self.features = Set()
        self.tests = Set()


    @property
    def chunks (self):
        chunk_sets = map (lambda f : frozenset(f.chunks), self.features)
        return reduce (lambda a, b : a.union(b), chunk_sets, set())
    
    
    @property
    def bugs (self):
        bug_sets = map (lambda c: frozenset(c.bugs), self.chunks)
        return reduce (lambda a, b : a.union(b), bug_sets, set())


    def add_feature(self, size):
        feature = Feature(self, size)
        self.features.add(feature)
        return feature


    def extend_feature(self, feature):
        feature.extend()


    def add_test(self,feature):
        test = Test(feature)
        self.tests.add(test) 
        return test


    def operate(self, random, limit=sys.maxint):
        
        successful_operations = 0
        
        if len(self.features) == 0:
            return successful_operations

        while successful_operations < limit:
            try:
                next_feature = random.sample(self.features,1)[0]
                next_feature.operate(random)
                successful_operations += 1
            except BugEncounteredException as e:
                return successful_operations
            except InoperableFeatureException as e:
                return successful_operations
            
        return limit


    def __str__(self):
        features_string = ",".join(map(lambda a : repr(a), self.features))
        return "[%s]" % features_string
