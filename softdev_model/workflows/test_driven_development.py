"""
@author: twsswt
"""

from .change_management import ChangeManagement
from specification import Specification
from .testing import Testing
from .implementation import Implementation
from .debugging import Debugging
from .refactoring import Refactoring


class TestDrivenDevelopment(Refactoring, Debugging, Implementation, Testing, Specification, ChangeManagement):

    def __init__(self,
                 centralised_vcs_server,
                 target_test_coverage_per_feature=1.0,
                 tests_per_chunk_ratio=1,
                 target_dependencies_per_feature=0
                 ):
        ChangeManagement.__init__(self, centralised_vcs_server)
        Specification.__init__(self, centralised_vcs_server)
        Testing.__init__(self, centralised_vcs_server, target_test_coverage_per_feature, tests_per_chunk_ratio)
        Implementation.__init__(self, centralised_vcs_server)
        Debugging.__init__(self, centralised_vcs_server)
        Refactoring.__init__(self, centralised_vcs_server, target_dependencies_per_feature)

    def implement_feature_tdd(self, feature_logical_name, feature_size, random):

        self.checkout()

        self.add_feature(feature_logical_name, feature_size, random)

        feature = self.centralised_vcs_client.working_copy.get_feature(feature_logical_name)

        self.test_per_chunk_ratio(feature, random)
        self.implement_feature(feature, random)
        self.debug_feature(feature, random)
        self.refactor_feature(feature, random)

    def allocate_tasks(self, schedule, random):
        """
        Implements the sequence of activities in a tests driven development workflow.
        """
        self.checkout()

        for logical_name, feature_size in schedule:
            self.implement_feature_tdd(logical_name, feature_size, random)
