import unittest

from nose_parameterized import parameterized, param

import fuzzi_moss
from fuzzi_moss import *

from softdev_model.system import Bug, Chunk, Feature, SoftwareProjectGroup, Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall
from softdev_model.workflows import waterfall
from softdev_model.workflows import test_driven_development


class TestCompareWorkFlows(unittest.TestCase):

    workflow_advice = {

        TestDrivenDevelopment.work:
            recurse_into_nested_steps(
                target_structures={ast.For, ast.TryExcept},
                fuzzer=filter_steps(
                    exclude_control_structures(),
                    fuzzer=choose_from([(0.95, identity), (0.05, remove_random_step)])
                )
            ),

        TestDrivenDevelopment._ensure_sufficient_tests:
            choose_from([(0.95, identity), (0.05, replace_condition_with(False))]),

        TestDrivenDevelopment._complete_feature:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))]),

        TestDrivenDevelopment._enhance_system_quality:
            choose_from([(0.95, identity), (0.05, remove_random_step)]),

        TestDrivenDevelopment._debug_feature:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))]),

        TestDrivenDevelopment._refactor_feature:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))]),

        Waterfall.work:
            choose_from([(0.5, identity), (0.5, remove_random_step)]),

        Waterfall._complete_specification:
            choose_from([(0.95, identity), (0.05, remove_random_step)]),

        Waterfall._implement_features:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))]),

        Waterfall._implement_test_suite:
            choose_from([(0.95, identity), (0.05, replace_condition_with(False))]),

        Waterfall._debug_system:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))]),

        Waterfall._refactor_system:
            choose_from([(0.99, identity), (0.01, replace_condition_with(False))])
    }

    @classmethod
    def setUpClass(cls):
        print "Workflow &" \
              "\tMean time to failure &" \
              "\tAllocated person time &" \
              "\tRemaining person time &" \
              "\tCompleted features &" \
              "\tSimulation Run time (ms) &" \
              "\tFuzzings applied.\\"

    def setUp(self):
        fuzzi_moss.fuzzi_moss_random.seed(1)
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

    @parameterized.expand(
        [
            param(workflow=Waterfall, person_time=50, advice={}),
            param(workflow=Waterfall, person_time=250, advice={}),
            param(workflow=Waterfall, person_time=500, advice={}),
            param(workflow=Waterfall, person_time=50, advice=workflow_advice),
            param(workflow=Waterfall, person_time=250, advice=workflow_advice),
            param(workflow=Waterfall, person_time=500, advice=workflow_advice),

            param(workflow=TestDrivenDevelopment, person_time=50, advice={}),
            param(workflow=TestDrivenDevelopment, person_time=250, advice={}),
            param(workflow=TestDrivenDevelopment, person_time=500, advice={}),
            param(workflow=TestDrivenDevelopment, person_time=50, advice=workflow_advice),
            param(workflow=TestDrivenDevelopment, person_time=250, advice=workflow_advice),
            param(workflow=TestDrivenDevelopment, person_time=500, advice=workflow_advice)
        ]
    )
    def test_compare_workflows(self, workflow, person_time, advice):

        def create_result_row(projects_group):
            return " & ".join([str(workflow.__name__),
                               str(person_time),
                               str(fuzzi_moss.enable_fuzzings),
                               str(projects_group.average_project_mean_time_to_failure),
                               str(projects_group.average_project_remaining_developer_time),
                               str(projects_group.average_project_features_implemented),
                               str(projects_group.duration)
                               ])

        fuzz_module(test_driven_development, advice)
        fuzz_module(waterfall, advice)

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


if __name__ == '__main__':
    unittest.main()
