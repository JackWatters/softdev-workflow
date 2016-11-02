"""
@author: twsswt
"""

from Queue import Empty

from theatre_ag import default_cost, Workflow

from .change_management import ChangeManagement
from specification import Specification
from .testing import Testing
from .implementation import Implementation
from .debugging import Debugging
from .refactoring import Refactoring


class TestDrivenDevelopment(Workflow):

    def __init__(self,
                 actor,
                 centralised_vcs_server,
                 target_test_coverage_per_feature=1.0,
                 tests_per_chunk_ratio=1,
                 target_dependencies_per_feature=0
                 ):

        Workflow.__init__(self, actor)

        self.change_management = ChangeManagement(actor, centralised_vcs_server)
        self.specification = Specification(actor, self.change_management)
        self.testing = Testing(actor, self.change_management, target_test_coverage_per_feature, tests_per_chunk_ratio)
        self.implementation = Implementation(actor, self.change_management)
        self.debugging = Debugging(actor, self.change_management)
        self.refactoring = Refactoring(actor, self.change_management, target_dependencies_per_feature)

    @default_cost()
    def implement_feature_tdd(self, user_story, random):
        """
        Implements the sequence of activities in a tests driven development workflow.
        """
        self.change_management.checkout()

        self.specification.add_feature(user_story.logical_name, user_story.size, random)

        feature = self.change_management.centralised_vcs_client.working_copy.get_feature(user_story.logical_name)

        self.testing.test_per_chunk_ratio(feature, random)
        self.implementation.implement_feature(feature, random)
        self.debugging.debug_feature(feature, random)
        self.refactoring.refactor_feature(feature, random)

    @default_cost()
    def work_from_backlog(self, product_backlog, random):

        while True:
            try:
                user_story = product_backlog.get(block=False)
                self.implement_feature_tdd(user_story, random)
            except Empty:
                break


