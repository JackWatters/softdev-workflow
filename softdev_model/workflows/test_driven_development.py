"""
@author: twsswt
"""

from specification import add_feature

from testing import test_per_chunk_ratio
from implementation import implement_feature
from debugging import debug_feature
from refactoring import refactor_feature


def implement_feature_tdd(
        self,
        centralised_vcs_client,
        feature_logical_name,
        feature_size,
        random,
        target_test_coverage_per_feature=1.0,
        tests_per_chunk_ratio=1,
        target_dependencies_per_feature=0):

    self.perform_task(add_feature, [centralised_vcs_client, feature_logical_name, feature_size, random])

    feature = centralised_vcs_client.working_copy.get_feature(feature_logical_name)

    self.perform_task(test_per_chunk_ratio,
                      [centralised_vcs_client, feature, random, target_test_coverage_per_feature, 1])

    self.perform_task(implement_feature, [centralised_vcs_client, feature, random])

    self.perform_task(debug_feature, [centralised_vcs_client, feature, random])

    self.perform_task(refactor_feature, [centralised_vcs_client, feature, random, target_dependencies_per_feature])


def test_driven_development(
        self,
        centralised_vcs_server,
        schedule,
        random,
        target_test_coverage_per_feature=1.0,
        tests_per_chunk_ratio=1,
        target_dependencies_per_feature=0):
        """
        Implements the sequence of activities in a tests driven development workflow.
        """
        centralised_vcs_client = centralised_vcs_server.checkout()

        for logical_name, feature_size in schedule:
            self.perform_task(implement_feature_tdd,
                [centralised_vcs_client, logical_name, feature_size, random,
                 target_test_coverage_per_feature, target_dependencies_per_feature])
