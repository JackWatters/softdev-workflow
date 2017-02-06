""""
@author: twsswt
"""

from theatre_ag import default_cost, Idling

from .change_management import ChangeManagement
from .implementation import Implementation
from .testing import Testing
from .debugging import Debugging
from .specification import Specification
from .refactoring import Refactoring


class Waterfall(object):

    is_workflow = True

    def __init__(self,
                 developers,
                 centralised_vcs_server,
                 target_test_coverage_per_feature=1.0,
                 tests_per_chunk_ratio=0,
                 target_dependencies_per_feature=1):

        self.developers = developers

        self.centralised_vcs_server = centralised_vcs_server
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.tests_per_chunk_ratio = tests_per_chunk_ratio
        self.target_dependencies_per_feature = target_dependencies_per_feature

        self.change_management = ChangeManagement(centralised_vcs_server)
        self.idling = Idling()

        self.pending_tasks = list()

    @default_cost()
    def choose_developer(self):
        if len(self.developers) == 0:
            return None

        chosen_developer = reduce(
            lambda d1, d2: d1 if d1.task_queue.qsize() < d2.task_queue.qsize() else d2, self.developers[1:])

        return chosen_developer

    def __repr__(self):
        return "Waterfall(%f, %d, %d)" % (
            self.target_test_coverage_per_feature,
            self.tests_per_chunk_ratio,
            self.target_dependencies_per_feature)

    def __str__(self):
        return "Waterfall"

    def _allocate_task(self, workflow, entry_point, arguments):
        developer = self.choose_developer()
        task = developer.allocate_task(workflow, entry_point, arguments)
        self.pending_tasks.append(task)

    def _allocate_specification_task(self, user_story, random):
        workflow = Specification(ChangeManagement(self.centralised_vcs_server))
        self._allocate_task(workflow, workflow.add_feature, [user_story.logical_name, user_story.size, random])

    def _allocate_implementation_task(self, feature, random):
        workflow = Implementation(ChangeManagement(self.centralised_vcs_server))
        self._allocate_task(workflow, workflow.implement_feature, [feature.logical_name, random])

    def _allocate_testing_task(self, feature, random):
        workflow = Testing(ChangeManagement(self.centralised_vcs_server))
        self._allocate_task(workflow, workflow.test_per_chunk_ratio, [feature.logical_name, random])

    def _allocate_debugging_task(self, feature, random):
        workflow = Debugging(ChangeManagement(self.centralised_vcs_server))
        self._allocate_task(workflow, workflow.debug_feature, [feature.logical_name, random])

    def _allocate_refactoring_task(self, feature, random):
        workflow = Refactoring(ChangeManagement(self.centralised_vcs_server))
        self._allocate_task(workflow, workflow.refactor_feature, [feature.logical_name, random])

    def wait_for_pending_tasks(self):
        for task in self.pending_tasks:
            self.idling.idle_until(task)

    @default_cost(1)
    def allocate_tasks(self, schedule, random):

        for user_story in schedule:
            self._allocate_specification_task(user_story, random)

        self.wait_for_pending_tasks()

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self._allocate_implementation_task(feature, random)

        self.wait_for_pending_tasks()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self._allocate_testing_task(feature, random)

        self.wait_for_pending_tasks()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self._allocate_debugging_task(feature, random)

        self.wait_for_pending_tasks()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self._allocate_debugging_task(feature, random)

        self.wait_for_pending_tasks()
