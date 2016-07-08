import unittest

from nose_parameterized import parameterized

import fuzzi_moss as fm

from random import Random

workflow_random = Random()

from fuzzi_moss.core_fuzzers import *

from softdev_model.system import Bug, Chunk, Feature, SoftwareProjectGroup, Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall


def create_experimental_parameters():

        result = list()

        workflows = [Waterfall, TestDrivenDevelopment]
        person_times = [50, 250, 500]
        p_incomplete_steps = [p / 100.0 for p in range(0, 100, 5)]
        p_miss_steps = [p / 100.0 for p in range(0, 100, 50)]

        for workflow in workflows:
            for person_time in person_times:
                for p_miss_step in p_miss_steps:
                    for p_incomplete_step in p_incomplete_steps:
                        result.append(( workflow, person_time, p_miss_step, p_incomplete_step))
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
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

    @parameterized.expand(create_experimental_parameters, testcase_func_name=test_name_func)
    def test_compare_workflows(self, workflow, person_time, p_miss_step, p_incomplete_step):

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

        def create_result_row(projects_group):
            return ", ".join(
                [
                    str(workflow.__name__),
                    str(person_time),
                    "%.2f" % p_miss_step,
                    "%.2f" % p_incomplete_step,
                    str(reduce(lambda i, j: i + j, fm.fuzzer_invocations.values(), 0)),
                    str(projects_group.average_project_mean_time_to_failure),
                    str(projects_group.average_project_remaining_developer_time),
                    str(projects_group.average_project_features_implemented),
                    "%.0f" % projects_group.duration
                ])

        fm.fuzz_clazz(workflow, workflow_advice)

        projects = \
            SoftwareProjectGroup(
                workflow=workflow,
                person_time=person_time,
                schedule=[3, 5, 7],
                number_of_traces=50,
                max_trace_length=750,
                n=10)

        projects.build_and_operate()
        print create_result_row(projects)
        fm.reset_invocation_counters()


if __name__ == '__main__':
    unittest.main()
