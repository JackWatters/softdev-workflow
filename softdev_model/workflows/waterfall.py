""""
@author: twsswt
"""

from theatre_ag import default_cost

from .change_management import ChangeManagement
from .implementation import Implementation
from .testing import Testing
from .debugging import Debugging
from .specification import Specification
from .refactoring import Refactoring


class Waterfall(Refactoring, Debugging, Implementation, Testing, Specification, ChangeManagement):

    def __init__(self,
                 centralised_vcs_server,
                 target_test_coverage_per_feature=1.0,
                 tests_per_chunk_ratio=0,
                 target_dependencies_per_feature=1):

        ChangeManagement.__init__(self, centralised_vcs_server)
        Specification.__init__(self, centralised_vcs_server)
        Implementation.__init__(self, centralised_vcs_server)
        Testing.__init__(self, centralised_vcs_server, target_test_coverage_per_feature, tests_per_chunk_ratio)
        Debugging.__init__(self, centralised_vcs_server)
        Refactoring.__init__(self, centralised_vcs_server, target_dependencies_per_feature)

    @default_cost()
    def allocate_tasks(
            self,
            schedule,
            random):
        """
        Implements the default_cost in a waterfall software development process.
        """
        self.complete_specification(schedule, random)
        self.implement_system(random)
        self.complete_system_test_suite(random)
        self.debug_system(random)
        self.refactor_system(random)


class AllocateTasks(object):

    def __init__(self, development_team):
        self.development_team = development_team

    @default_cost()
    def choose_developer(self):
        if len(self.development_team.developers) == 0:
            return None
        chosen_developer = reduce(lambda d1, d2: len(), self.development_team.developers)

        return chosen_developer

    @default_cost()
    def allocate_tasks(self, schedule, random):
        self.checkout()

        for logical_name, feature_size in schedule:
            developer = self.choose_developer()
            developer.allocate_task(developer.implement_feature_tdd, [logical_name, feature_size, random])
