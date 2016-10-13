""""
@author: twsswt
"""
from softdev_model.system import BugEncounteredException, CentralisedVCSException


class Waterfall(object):
    """
    Implements the workflow in a waterfall software development process.
    """

    def __init__(self,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0,
                 target_minimum_tests_per_chunk=1
                 ):
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature
        self.target_minimum_tests_per_chunk = target_minimum_tests_per_chunk

        self.chunk_count = 0
        self.test_count = 0

    def work(self, centralised_vcs_server, developer, schedule, random):

        centralised_vcs_client = centralised_vcs_server.checkout()

        self._complete_specification(developer, schedule, centralised_vcs_client, random)
        self._implement_features(developer, centralised_vcs_client, random)

        self._implement_test_suite(developer, centralised_vcs_client, random)
        self._debug_system(developer, centralised_vcs_client, random)
        self._refactor_system(developer, centralised_vcs_client, random)

    def _complete_specification(self, developer, schedule, centralised_vcs_client, random):
        for logical_name, feature_size in schedule:
            centralised_vcs_client.working_copy.add_feature(logical_name=logical_name, size=feature_size)
            self._commit_changes(developer, centralised_vcs_client, random)

    def _implement_features(self, developer, centralised_vcs_client, random):

        for feature in centralised_vcs_client.working_copy.features:
            while not feature.is_implemented:
                developer.extend_feature(self.chunk_count, feature, random)
                self.chunk_count += 1
                self._commit_changes(developer, centralised_vcs_client, random)

    def _implement_test_suite(self, developer, centralised_vcs_client, random):

        for feature in centralised_vcs_client.working_copy.features:
            while feature.test_coverage < self.target_test_coverage_per_feature or \
                    feature.minimum_tests_per_chunk < self.target_minimum_tests_per_chunk:

                centralised_vcs_client.update(developer, random)

                developer.add_test(feature.software_system, self.test_count, feature)
                self.test_count += 1

                self._commit_changes(developer, centralised_vcs_client, random)

    def _debug_system(self, developer, centralised_vcs_client, random):

        for test in centralised_vcs_client.working_copy.tests:
            while True:
                try:
                    test.exercise()
                    break
                except BugEncounteredException as e:
                    developer.debug(test.feature, e.bug, random)
                    self._commit_changes(developer, centralised_vcs_client, random)

    def _refactor_system(self, developer, centralised_vcs_client, random):
        for feature in centralised_vcs_client.working_copy.features:
            while len(feature.dependencies) > self.target_dependencies_per_feature:
                developer.refactor(feature, random)
                self._commit_changes(developer, centralised_vcs_client, random)

    @staticmethod
    def _commit_changes(developer, centralised_vcs_client, random):
        while True:
            try:
                centralised_vcs_client.commit()
                centralised_vcs_client.update(developer, random)
                break
            except CentralisedVCSException:
                centralised_vcs_client.update(developer, random)
                for conflict in centralised_vcs_client.conflicts:
                    developer.resolve_conflict(centralised_vcs_client, conflict, random)

