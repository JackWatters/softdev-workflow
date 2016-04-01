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


    def work(self, random, software_developer):

        # Implement features
        for feature in self.software_system.features:
            while not feature.is_implemented:
                self.software_system.extend_feature(feature, random)

        #Implement test suite
        for feature in self.software_system.features:
            while len(feature.tests) < feature.size * self.target_tests_per_feature:
                self.software_system.add_test(feature)

        # Debug
        for test in self.software_system.tests:
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    test.feature.debug(random, e.bug)

        # Refactor
        for feature in self.software_system.features:
            for _ in range (0,self.target_refactorings_per_feature):
                feature.refactor(random)


    def deliver (self):
        return self.software_system