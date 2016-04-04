'''
Created on 23 Mar 2016

@author: Tim
'''
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.bug import BugEncounteredException


class Waterfall(object):
    '''
    Represents a waterfall software development process.
    '''

    def __init__(self, 
                 project_characteristics, 
                 project_schedule, 
                 target_tests_per_feature, 
                 target_refactorings_per_feature):

        self.target_tests_per_feature = target_tests_per_feature
        self.target_refactorings_per_feature = target_refactorings_per_feature

        self.software_system = SoftwareSystem(project_characteristics)

        for feature_size in project_schedule:
            self.software_system.add_feature(feature_size)


    def work(self, random, developer):

        # Implement features
        for feature in self.software_system.features:
            while not feature.is_implemented:
                developer.extend_feature(random, feature)

        #Implement test suite
        for feature in self.software_system.features:
            while len(feature.tests) < feature.size * self.target_tests_per_feature:
                developer.add_test(self.software_system, feature)

        # Debug
        for test in self.software_system.tests:
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    developer.debug(random, test, e.bug)

        # Refactor
        for feature in self.software_system.features:
            for _ in range (0,self.target_refactorings_per_feature):
                developer.refactor(random, feature)


    def deliver (self):
        return self.software_system