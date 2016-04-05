'''
Created on 23 Mar 2016

@author: Tim
'''
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.bug import BugEncounteredException


class Waterfall(object):
    """
    Represents a waterfall software development process.
    """

    def __init__(self,
                 software_system,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0):
        self.software_system = software_system
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    def work(self, random, developer):

        # Implement features
        for feature in self.software_system.features:
            while not feature.is_implemented:
                developer.extend_feature(random, feature)

        # Implement test suite
        for feature in self.software_system.features:
            while feature.test_coverage < self.target_test_coverage_per_feature:
                developer.add_test(feature)

        # Debug
        for test in self.software_system.tests:
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    developer.debug(random, test.feature, e.bug)

        # Refactor
        for feature in self.software_system.features:
            while len(feature.dependencies) > self.target_dependencies_per_feature:
                developer.refactor(random, feature)

    def deliver (self):
        return self.software_system
