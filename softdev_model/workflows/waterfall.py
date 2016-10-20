""""
@author: twsswt
"""

from .specification import complete_specification
from .implementation import implement_system
from .testing import complete_system_test_suite
from .debugging import debug_system
from .refactoring import refactor_system


def waterfall(
        self,
        centralised_vcs_server,
        schedule,
        random,
        target_test_coverage_per_feature=1.0,
        target_dependencies_per_feature=0,
        tests_per_chunk_ratio=1):
        """
        Implements the workflow in a waterfall software development process.
        """

        centralised_vcs_client = centralised_vcs_server.checkout()
        self.perform_task(complete_specification, [schedule, centralised_vcs_client, random])
        self.perform_task(implement_system, [centralised_vcs_client, random])

        self.perform_task(
            complete_system_test_suite,
              [centralised_vcs_client, random,
               target_test_coverage_per_feature,
               tests_per_chunk_ratio])

        self.perform_task(debug_system, [centralised_vcs_client, random])
        self.perform_task(refactor_system, [centralised_vcs_client, random, target_dependencies_per_feature])
