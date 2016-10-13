"""
@author: twsswt
"""

from softdev_model.system import BugEncounteredException, DeveloperExhaustedException


class TestDrivenDevelopment(object):
    """
    Represents the sequence of activities in a tests driven development workflow.
    """

    def __init__(self,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0):

        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature
        self.chunk_count = 0

    def work(self, random, software_system, developer, schedule):
        # Complete main tasks.
        for logical_name, feature_size in schedule:
            feature = software_system.add_feature(logical_name, feature_size)
            try:
                self._ensure_sufficient_tests(developer, feature)
                self._complete_feature(developer, feature, random)
                self._refactor_feature(developer, feature, random)
            except DeveloperExhaustedException:
                software_system.features.remove(feature)

    def _ensure_sufficient_tests(self, developer, feature):
        while feature.test_coverage < self.target_test_coverage_per_feature:
            developer.add_test(feature.software_system, len(feature.tests), feature)

    def _complete_feature(self, developer, feature, random):
        while not feature.is_implemented:
            developer.extend_feature(self.chunk_count, feature, random)
            self.chunk_count += 1
            self._debug_feature(developer, feature, random)

    @staticmethod
    def _debug_feature(developer, feature, random):
        while True:
            try:
                feature.exercise_tests()
                break
            except BugEncounteredException as e:
                developer.debug(feature, e.bug, random)

    def _refactor_feature(self, developer, feature, random):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            developer.refactor(feature, random)
