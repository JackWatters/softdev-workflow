""""
@author: twsswt
"""
from softdev_model.system import BugEncounteredException


class Waterfall(object):
    """
    Represents a waterfall software development process.
    """

    def __init__(self,
                 software_system,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0
                 ):
        self.software_system = software_system
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    def work(self, random, developer, schedule):
        # Complete specification
        for feature_size in schedule:
            self.software_system.add_feature(feature_size)

        # Implement features
        for feature in self.software_system.features:
            while not feature.is_implemented:
                developer.extend_feature(random, feature)

        # Implement tests suite
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
