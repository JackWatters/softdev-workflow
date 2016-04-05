"""
@author: tws
"""
from models.systems.software.bug import BugEncounteredException


class TestDrivenDevelopment(object):
    def __init__(self,
                 software_system,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0):

        self.software_system = software_system
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    def work(self, random, developer):
        for feature in self.software_system.features:
            self._ensure_sufficient_tests(developer, feature)
            self._complete_feature(random, developer, feature)
            self._refactor_feature(random, developer, feature)

    def _ensure_sufficient_tests(self, developer, feature):
        while feature.test_coverage < self.target_test_coverage_per_feature:
            developer.add_test(feature)

    def _complete_feature(self, random, developer, feature):
        while not feature.is_implemented:
            developer.extend_feature(random, feature)
            while True:
                try:
                    feature.exercise_tests()
                    break
                except BugEncounteredException as e:
                    developer.debug(random, feature, e.bug)

    def _refactor_feature(self, random, developer, feature):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            developer.refactor(random, feature)
