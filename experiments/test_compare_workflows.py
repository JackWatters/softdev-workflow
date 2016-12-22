import unittest

from nose_parameterized import parameterized

from Queue import Queue

import pydysofu

from fuzzi_moss import missed_target
from fuzzi_moss.socio_technical_fuzzers import workflow_actors_name_is

from softdev_model.system import SoftwareProjectGroup, SystemRandom, TestDrivenDevelopmentPlan, UserStory, \
    WaterfallDevelopmentPlan

from softdev_model.workflows import ChangeManagement, Debugging, Implementation, Refactoring, Specification, Testing, \
    TestDrivenDevelopment, Waterfall


random = SystemRandom(1)

schedule = [UserStory(0, 3, 1), UserStory(1, 5, 2), UserStory(2, 7, 3)]

product_backlog = Queue()
for user_story in schedule: product_backlog.put(user_story)

waterfall_plan = WaterfallDevelopmentPlan(schedule, random)
tdd_plan = TestDrivenDevelopmentPlan(product_backlog, random)


def create_short_experimental_parameters():
    return [
        (plan, team_size, max_clock_tick, p_miss_step, p_incomplete_step)
        for plan in [waterfall_plan]
        for team_size in [2]
        for max_clock_tick in [300]
        for p_miss_step in [0.0]
        for p_incomplete_step in [1.0]
    ]


def create_full_experimental_parameters():
    return [
        (plan, team_size, max_clock_tick, p_miss_step, p_incomplete_step)
        for plan in [waterfall_plan, tdd_plan]
        for team_size in [1, 2, 5, 10]
        for max_clock_tick in [150, 300, 500]
        for p_miss_step in [p / 100.0 for p in range(0, 100, 50)]
        for p_incomplete_step in [p / 100.0 for p in range(0, 100, 5)]
    ]


def test_name_func(func, param_num, param):
    return "%s_%03d" % (func.__name__, param_num)


class TestCompareWorkFlows(unittest.TestCase):

    @staticmethod
    def run_experiment(plan, number_of_developers, number_of_clock_ticks, p_miss_step, p_incomplete_step):

        workflow_random = SystemRandom()

        workflow_advice = {

            ChangeManagement.commit_changes: {workflow_actors_name_is('alice'): missed_target(workflow_random)}


            #    in_sequence({
            #        insert_steps(0, 'from random import Random\ncommit_random=Random(1)'),
            #        replace_condition_with('commit_random.random() < 0.75')
            #    })

            #ChangeManagement.resolve: identity,
            #ChangeManagement.checkout: identity,

            #Specification.add_feature: identity,
            #Implementation.implement_feature: identity,
            #Testing.test_per_chunk_ratio: identity,
            #Debugging.debug_feature: identity,
            #Refactoring.refactor_feature: identity,

            #TestDrivenDevelopment.implement_feature_tdd:
            #    recurse_into_nested_steps(
            #        target_structures={ast.For, ast.TryExcept},
            #        fuzzer=filter_steps(
            #            exclude_control_structures(),
            #            fuzzer=choose_from([(p_miss_step, remove_random_step), (1 - p_miss_step, identity)])
            #        )
            #    ),

            #TestDrivenDevelopment.work_from_backlog: identity,
            #TestDrivenDevelopment.implement_feature_tdd: identity,
            #Waterfall.allocate_tasks: identity,
        }

        pydysofu.fuzz_clazz(ChangeManagement, workflow_advice)

        #fm.fuzz_clazz(Specification, workflow_advice)
        #fm.fuzz_clazz(Implementation, workflow_advice)
        #fm.fuzz_clazz(Testing, workflow_advice)
        #fm.fuzz_clazz(Debugging, workflow_advice)
        #fm.fuzz_clazz(Refactoring, workflow_advice)

        #fm.fuzz_clazz(Waterfall, workflow_advice)
        #fm.fuzz_clazz(TestDrivenDevelopment, workflow_advice)

        projects_group = \
            SoftwareProjectGroup(
                plan,
                workflow_random,
                number_of_developers,
                number_of_clock_ticks,
                number_of_projects=1,
                number_of_traces=1,
                max_trace_length=750)

        projects_group.build_and_operate()

        print "%s, %d, %d, %.2f, %.2f, %d, %d, %d, %.2f, %d" % \
            (
                plan.__class__.__name__,
                number_of_clock_ticks,
                number_of_developers,
                p_miss_step,
                p_incomplete_step,
                pydysofu.fuzzer_invocations_count(),
                projects_group.average_project_mean_time_to_failure,
                projects_group.average_project_remaining_developer_time,
                projects_group.average_project_features_implemented,
                projects_group.simulation_duration

            )

        pydysofu.reset_invocation_counters()

    @classmethod
    def setUpClass(cls):
        print ", ".join(
            [
                "workflow",
                "allocated time",
                "team size,"
                "p miss step",
                "p not finish",
                "fuzzings applied",
                "mean time to failure",
                "remaining_time",
                "completed features",
                "run time(s)"
            ])

    def setUp(self):
        pydysofu.pydysofu_random.seed(1)

    #@parameterized.expand(create_full_experimental_parameters, testcase_func_name=test_name_func)
    @parameterized.expand(create_short_experimental_parameters, testcase_func_name=test_name_func)
    def test_compare_workflows_short_parameters(
            self, plan, number_of_developers, number_of_clock_ticks, p_miss_step, p_incomplete_step):
        self.run_experiment(plan, number_of_developers, number_of_clock_ticks, p_miss_step, p_incomplete_step)

if __name__ == '__main__':
    unittest.main()
