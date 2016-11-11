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

    @default_cost()
    def choose_developer(self):
        if len(self.developers) == 0:
            return None

        chosen_developer = reduce(
            lambda d1, d2: d1 if d1.task_queue.qsize() < d2.task_queue.qsize() else d2,
            self.developers[1:])
        return chosen_developer

    def __repr__(self):
        return "Waterfall(%f, %d, %d)" % (
            self.target_test_coverage_per_feature,
            self.tests_per_chunk_ratio,
            self.target_dependencies_per_feature)

    def __str__(self):
        return "Waterfall"

    @default_cost(1)
    def allocate_tasks(self, schedule, random):

        tasks = set()

        for user_story in schedule:

            developer = self.choose_developer()
            specification_task = Specification(ChangeManagement(self.centralised_vcs_server))
            task = developer.allocate_task(
                specification_task, specification_task.add_feature,
                [user_story.logical_name, user_story.size, random])

            tasks.add(task)

        for task in tasks:
            self.idling.idle_until(task)

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:

            developer = self.choose_developer()
            implementation_task = Implementation(ChangeManagement(self.centralised_vcs_server))

            task = developer.allocate_task(
                implementation_task, implementation_task.implement_feature, [feature.logical_name, random])

            tasks.add(task)

        for task in tasks:
            self.idling.idle_until(task)

        for feature in self.change_management.centralised_vcs_client.working_copy.features:

            developer = self.choose_developer()
            testing_task = Testing(ChangeManagement(self.centralised_vcs_server))

            task = developer.allocate_task(
                testing_task, testing_task.test_per_chunk_ratio, [feature.logical_name, random])

            tasks.add(task)

        for task in tasks:
            self.idling.idle_until(task)

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            developer = self.choose_developer()
            debugging_task = Debugging(ChangeManagement(self.centralised_vcs_server))

            task = developer.allocate_task(
                debugging_task, debugging_task.debug_feature, [feature.logical_name, random])

            tasks.add(task)

        for task in tasks:
            self.idling.idle_until(task)

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            developer = self.choose_developer()
            refactoring_task = Refactoring(ChangeManagement(self.centralised_vcs_server))

            task = developer.allocate_task(
                refactoring_task, refactoring_task.refactor_feature, [feature.logical_name, random])

            tasks.add(task)

        for task in tasks:
            self.idling.idle_until(task)

