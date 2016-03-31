'''
Created on 23 Mar 2016

@author: Tim
'''
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.bug import BugEncounteredException


class Waterfall(object):
    '''
    classdocs
    '''

    def __init__(self, project_schedule):

        self.software_system = SoftwareSystem()

        for feature_size in project_schedule:
            self.software_system.add_feature(feature_size)


    def work(self, random, software_developer):

        features = self.software_system.features

        # Implement features
        for feature in sorted(features, key=lambda f : f.id ):
            while not feature.is_implemented:
                self.software_system.extend_feature(feature, random)
        
        #Implement test suite
        for feature in sorted(features, key=lambda f : f.id):
            while len(feature.test_coverage) < len(feature.chunks) or len(feature.tests) < feature.size * 2.5:
                self.software_system.add_test(feature)
                

        # Debug
        for test in sorted(self.software_system.tests, key=lambda t : t.id):
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    test.feature.debug(random, e.bug)
        
        # Refactor
        for feature in sorted(features, key=lambda f : f.id):
            for _ in range (0,199):
                feature.refactor(random)
        

    def deliver (self):
        return self.software_system