'''
@author: tws
'''
import sys
from feature import Feature
from test import Test
from bug import BugEncounteredException
from models.systems.software.feature import InoperableFeatureException
from sortedcontainers.sortedset import SortedSet

class SoftwareSystem:


    def __init__(self,
                 probabilities={
                    'gain_feature_dependency':0.5,
                    'lose_feature_dependency':0.25,
                    'gain_system_dependency':0.1,
                    'lose_system_dependency':0.25,
                    'new_bug':0.5,
                    'debug_known':0.9,
                    'debug_unknown':0.01,
                    'failure_on_demand':0.01,
                    'coverage' : 0.5,
                    'detection':0.5
                }):
        
        self.probabilities = probabilities
        self.features = SortedSet(key=lambda f : f.id)
        self.tests = SortedSet(key=lambda t : t.id)


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


    def extend_feature(self, feature, random):
        feature.extend(random)


    def add_test(self,feature):
        test = Test(feature)
        self.tests.add(test) 
        return test


    def operate(self, random, limit=sys.maxint):
        
        successful_operations = []
        
        if len(self.features) == 0:
            return successful_operations
                    
        while len(successful_operations) < limit:
            try:
                next_feature = random.choice(self.features)
                next_feature.operate(random)
                successful_operations.append(next_feature)
            except BugEncounteredException as e:
                return successful_operations
            except InoperableFeatureException as e:
                return successful_operations
            
        return successful_operations


    def __str__(self):
        features_string = ",".join(map(lambda a : repr(a), self.features))
        return "[%s]" % features_string
