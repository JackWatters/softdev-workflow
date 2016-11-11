import unittest

from nose_parameterized import parameterized

from Queue import Queue

import fuzzi_moss as fm

from fuzzi_moss.core_fuzzers import *

from softdev_model.system import SoftwareProjectGroup, SystemRandom, TestDrivenDevelopmentPlan, UserStory
from softdev_model.workflows import ChangeManagement, Debugging, Implementation, Refactoring, Specification, Testing, \
    TestDrivenDevelopment, Waterfall

workflow_random = SystemRandom()


def create_experimental_parameters():

        result = list()

        number_of_clock_tickss = [50, 250]
        number_of_developerss = [2, 5, 10]
        p_incomplete_steps = [p / 100.0 for p in range(0, 100, 5)]
        p_miss_steps = [p / 100.0 for p in range(0, 100, 50)]

        number_of_clock_tickss = [500]
        number_of_developerss = [2]
        p_incomplete_steps = [p / 100.0 for p in range(0, 100, 100)]
        p_miss_steps = [p / 100.0 for p in range(0, 100, 100)]

        for number_of_developers in number_of_developerss:
            for number_of_clock_ticks in number_of_clock_tickss:
                for p_miss_step in p_miss_steps:
                    for p_incomplete_step in p_incomplete_steps:
                        result.append(
                            (number_of_developers, number_of_clock_ticks, p_miss_step, p_incomplete_step))
        return result


def test_name_func(testcase_func, param_num, param):
    return "%s_%03d" % (testcase_func.__name__, param_num)


class TestCompareWorkFlows(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        print ", ".join(
            [
                "workflow",
                "allocated time",
                "p miss step",
                "p not finish",
                "fuzzings applied",
                "mean time to failure",
                "remaining_time",
                "completed features",
                "run time(s)"
             ])

    def setUp(self):
        fm.fuzzi_moss_random.seed(1)

    @parameterized.expand(create_experimental_parameters, testcase_func_name=test_name_func)
    def test_compare_workflows(self, number_of_developers, number_of_clock_ticks, p_miss_step, p_incomplete_step):

        incomplete_step_fuzzer = \
            recurse_into_nested_steps(
                target_structures={ast.For, ast.TryExcept},
                fuzzer=filter_steps(
                    exclude_control_structures(target={ast.For}),
                    choose_from(
                    [
                        (1 - p_incomplete_step, identity),
                        (p_incomplete_step, replace_condition_with(False))
                    ]
                    )
                )
            )

        '''
        workflow_advice = {
            TestDrivenDevelopment.work:
                recurse_into_nested_steps(
                    target_structures={ast.For, ast.TryExcept},
                    fuzzer=filter_steps(
                        exclude_control_structures(),
                        fuzzer=choose_from([(p_miss_step, remove_random_step), (1 - p_miss_step, identity)])
                    )
                ),

            TestDrivenDevelopment._ensure_sufficient_tests: incomplete_step_fuzzer,
            TestDrivenDevelopment._complete_feature: incomplete_step_fuzzer,
            TestDrivenDevelopment._enhance_system_quality: incomplete_step_fuzzer,
            TestDrivenDevelopment._debug_feature: incomplete_step_fuzzer,
            TestDrivenDevelopment._refactor_feature: incomplete_step_fuzzer,

            Waterfall.work:
                choose_from([(p_miss_step, remove_random_step), (1 - p_miss_step, identity)]),

            Waterfall._implement_features: incomplete_step_fuzzer,
            Waterfall._implement_test_suite: incomplete_step_fuzzer,
            Waterfall._debug_system: incomplete_step_fuzzer,
            Waterfall._refactor_system: incomplete_step_fuzzer,
        }
        '''
        workflow_advice = {
            TestDrivenDevelopment.implement_feature_tdd :
                recurse_into_nested_steps(
                    target_structures={ast.For, ast.TryExcept},
                    fuzzer=filter_steps(
                        exclude_control_structures(),
                        fuzzer=choose_from([(p_miss_step, remove_random_step), (1 - p_miss_step, identity)])
                    )
                ),
        }

        def create_result_row(projects_group):

            return ", ".join(
                [
                    str(plan.__class__.__name__),
                    str(number_of_clock_ticks),
                    "%.2f" % p_miss_step,
                    "%.2f" % p_incomplete_step,
                    str(reduce(lambda i, j: i + j, fm.fuzzer_invocations.values(), 0)),
                    str(projects_group.average_project_mean_time_to_failure),
                    str(projects_group.average_project_remaining_developer_time),
                    str(projects_group.average_project_features_implemented),
                    "%.0f" % projects_group.duration
                ])

        #fm.fuzz_clazz(Waterfall, workflow_advice)
        fm.fuzz_clazz(TestDrivenDevelopment, workflow_advice)
        #fm.fuzz_clazz(Specification, workflow_advice)
        #fm.fuzz_clazz(Implementation, workflow_advice)
        #fm.fuzz_clazz(Testing, workflow_advice)
        #fm.fuzz_clazz(Debugging, workflow_advice)
        #fm.fuzz_clazz(Refactoring, workflow_advice)
        #fm.fuzz_clazz(ChangeManagement, workflow_advice)

        product_backlog = Queue()

        product_backlog.put(UserStory(0, 3, 1))
        product_backlog.put(UserStory(1, 5, 2))
        product_backlog.put(UserStory(2, 7, 3))

        plan = TestDrivenDevelopmentPlan(product_backlog, workflow_random)

        projects = \
            SoftwareProjectGroup(
                plan, number_of_developers, number_of_clock_ticks, number_of_traces=1, max_trace_length=750, n=1)

        projects.build_and_operate()

        print create_result_row(projects)
        fm.reset_invocation_counters()


if __name__ == '__main__':
    unittest.main()
