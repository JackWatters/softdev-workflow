import unittest

from nose_parameterized import parameterized, param

import fuzzi_moss

from softdev_model.system import Bug, Chunk, Feature, SoftwareProjectGroup, Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall


class TestCompareWorkFlows(unittest.TestCase):

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
            param(workflow=Waterfall, person_time=50, enable_fuzzings=False),
            param(workflow=Waterfall, person_time=250, enable_fuzzings=False),
            param(workflow=Waterfall, person_time=500, enable_fuzzings=False),
            param(workflow=Waterfall, person_time=50, enable_fuzzings=True),
            param(workflow=Waterfall, person_time=250, enable_fuzzings=True),
            param(workflow=Waterfall, person_time=500, enable_fuzzings=True),

            param(workflow=TestDrivenDevelopment, person_time=50, enable_fuzzings=False),
            param(workflow=TestDrivenDevelopment, person_time=250, enable_fuzzings=False),
            param(workflow=TestDrivenDevelopment, person_time=500, enable_fuzzings=False),
            param(workflow=TestDrivenDevelopment, person_time=50, enable_fuzzings=True),
            param(workflow=TestDrivenDevelopment, person_time=250, enable_fuzzings=True),
            param(workflow=TestDrivenDevelopment, person_time=500, enable_fuzzings=True)
        ]
    )
    def test_compare_workflows(self, workflow, person_time, enable_fuzzings):

        def create_result_row(projects_group):
            return " & ".join([str(workflow.__name__),
                               str(person_time),
                               str(fuzzi_moss.enable_fuzzings),
                               str(projects_group.average_project_mean_time_to_failure),
                               str(projects_group.average_project_remaining_developer_time),
                               str(projects_group.average_project_features_implemented),
                               str(projects_group.duration)
                               ])

        projects = \
            SoftwareProjectGroup(
                workflow=workflow,
                person_time=person_time,
                schedule=[3, 5, 7],
                number_of_traces=50,
                max_trace_length=750,
                n=10)

        fuzzi_moss.enable_fuzzings = enable_fuzzings

        projects.build_and_operate()

        print create_result_row(projects)




if __name__ == '__main__':
    unittest.main()
