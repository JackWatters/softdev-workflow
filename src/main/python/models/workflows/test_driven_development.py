"""
@author: tws
"""
from models.systems.software.bug import BugEncounteredException
from models.systems.software.developer import DeveloperExhaustedException


class TestDrivenDevelopment(object):
    def __init__(self,
                 software_system,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0):

        self.software_system = software_system
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    def work(self, random, developer, schedule):
        # Complete main tasks.
        for feature_size in schedule:
            feature = self.software_system.add_feature(feature_size)
            self._ensure_sufficient_tests(developer, feature)
            self._complete_feature(random, developer, feature)
            self._refactor_feature(random, developer, feature)

        # Work in wider quality assurance.
        #while True:
        #    try:
        #        self._enhance_system_quality(random, developer)
        #    except DeveloperExhaustedException:
        #        break

    def _ensure_sufficient_tests(self, developer, feature):
        while feature.test_coverage < self.target_test_coverage_per_feature:
            developer.add_test(feature)

    def _complete_feature(self, random, developer, feature):
        while not feature.is_implemented:
            developer.extend_feature(random, feature)
            self._debug_feature(random, developer, feature)

    def _enhance_system_quality(self, random, developer):
        feature = random.choice(self.software_system.features)
        developer.add_test(feature)
        self._debug_feature(random, developer, feature)
        self._refactor_feature(random, developer, feature)

    @staticmethod
    def _debug_feature(random, developer, feature):
        while True:
            try:
                feature.exercise_tests()
                break
            except BugEncounteredException as e:
                developer.debug(random, feature, e.bug)

    def _refactor_feature(self, random, developer, feature):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            developer.refactor(random, feature)
