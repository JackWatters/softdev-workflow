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

        self.chunk_count = 0

    def work(self, random, centralised_vcs_server, developer, schedule):

        self._complete_specification(developer, random, schedule, centralised_vcs_server)
        self._implement_features(developer, random, centralised_vcs_server)
        self._implement_test_suite(developer, centralised_vcs_server)
        #self._debug_system(developer, random, centralised_vcs_server)
        #self._refactor_system(developer, random, centralised_vcs_server)

    @staticmethod
    def _complete_specification(developer, random, schedule, centralised_vcs_server):
        for logical_name, feature_size in schedule:
            centralised_vcs_client = centralised_vcs_server.checkout()
            centralised_vcs_client.working_copy.add_feature(logical_name=logical_name, size=feature_size)
            centralised_vcs_client.update(random)
            centralised_vcs_client.commit()

    def _implement_features(self, developer, random, centralised_vcs_server):
        centralised_vcs_client = centralised_vcs_server.checkout()

        for feature in centralised_vcs_client.working_copy.features:
            while not feature.is_implemented:
                centralised_vcs_client.update(random)
                developer.extend_feature(random, self.chunk_count, feature)
                self.chunk_count += 1
                centralised_vcs_client.update(random)
                centralised_vcs_client.commit()

    def _implement_test_suite(self, developer, centralised_vcs_server):

        centralised_vcs_client = centralised_vcs_server.checkout()

        for feature in centralised_vcs_client.working_copy.features:
            while feature.test_coverage < self.target_test_coverage_per_feature:
                developer.add_test(feature.software_system, feature)

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


