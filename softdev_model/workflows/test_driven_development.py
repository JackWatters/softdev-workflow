"""
@author: twsswt
"""

from Queue import Empty

from theatre_ag import default_cost

from .change_management import ChangeManagement
from specification import Specification
from .testing import Testing
from .implementation import Implementation
from .debugging import Debugging
from .refactoring import Refactoring


class TestDrivenDevelopment():

    is_workflow = True

    def __init__(self,
                 centralised_vcs_server,
                 target_test_coverage_per_feature=1.0,
                 tests_per_chunk_ratio=1,
                 target_dependencies_per_feature=0
                 ):

        change_management = ChangeManagement(centralised_vcs_server)
        self.specification = Specification(change_management)
        self.testing = Testing(change_management, target_test_coverage_per_feature, tests_per_chunk_ratio)
        self.implementation = Implementation(change_management)
        self.debugging = Debugging(change_management)
        self.refactoring = Refactoring(change_management, target_dependencies_per_feature)

    @default_cost()
    def implement_feature_tdd(self, user_story, random):
        """
        Implements the sequence of activities in a tests driven development workflow.
        """
        self.specification.add_feature(user_story.logical_name, user_story.size, random)
        self.testing.test_per_chunk_ratio(user_story.logical_name, random)
        self.implementation.implement_feature(user_story.logical_name, random)
        self.debugging.debug_feature(user_story.logical_name, random)
        self.refactoring.refactor_feature(user_story.logical_name, random)

    @default_cost()
    def work_from_backlog(self, product_backlog, random):

        while True:
            try:
                user_story = product_backlog.get(block=False)
                self.implement_feature_tdd(user_story, random)
            except Empty:
                break


