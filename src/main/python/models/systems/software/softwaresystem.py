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
        probability_gain_feature_dependency = 0.1,
        probability_gain_system_dependency = 0.05,
        probability_lose_feature_dependency = 0.05,
        probability_lose_system_dependency = 0.05,

        probability_new_bug = 0.5,
        probability_debug_known=0.9,
        probability_debug_unknown=0.01,
        pfd=0.01,
        pdetect=0.5
        
        ):
        
        self.probability_gain_feature_dependency = probability_gain_feature_dependency
        self.probability_gain_system_dependency = probability_gain_system_dependency

        self.probability_lose_feature_dependency = probability_lose_feature_dependency
        self.probability_lose_system_dependency = probability_lose_system_dependency

        self.probability_new_bug = probability_new_bug
        self.probability_debug_known=probability_debug_known
        self.probability_debug_unknown=probability_debug_unknown
        
        self.pfd = pfd
        self.pdetect = pdetect

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
