""""
@author: twsswt
"""
from softdev_model.system import BugEncounteredException


class Waterfall(object):
    """
    Represents a waterfall software development process.
    """

    def __init__(self,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0
                 ):
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    def work(self, random, software_system, developer, schedule):

        self._complete_specification(schedule, software_system)
        self._implement_features(developer, random, software_system)
        self._implement_test_suite(developer, software_system)
        self._debug_system(developer, random, software_system)
        self._refactor_system(developer, random, software_system)

    @staticmethod
    def _complete_specification(schedule, software_system):
        for feature_size in schedule:
            software_system.add_feature(feature_size)

    @staticmethod
    def _implement_features(developer, random, software_system):
        for feature in software_system.features:
            while not feature.is_implemented:
                developer.extend_feature(random, feature)

    def _implement_test_suite(self, developer, software_system):
        for feature in software_system.features:
            while feature.test_coverage < self.target_test_coverage_per_feature:
                developer.add_test(feature)

    @staticmethod
    def _debug_system(developer, random, software_system):
        for test in software_system.tests:
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    developer.debug(random, test.feature, e.bug)

    def _refactor_system(self, developer, random, software_system):
        for feature in software_system.features:
            while len(feature.dependencies) > self.target_dependencies_per_feature:
                developer.refactor(random, feature)


