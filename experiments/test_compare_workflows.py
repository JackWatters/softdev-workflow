import unittest

import fuzzi_moss

from random import Random

from softdev_model.system import Bug, Chunk, Developer, Feature, SoftwareProjectGroup, Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall


class TestCompareWorkFlows(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.waterfall_projects =\
            SoftwareProjectGroup(
                workflow=Waterfall,
                person_time=250,
                schedule=[3,5,7],
                number_of_traces=50,
                max_trace_length=750,
                n=10)

        self.tdd_projects = \
            SoftwareProjectGroup(
                workflow=TestDrivenDevelopment,
                person_time=250,
                schedule=[3, 5, 7],
                number_of_traces=50,
                max_trace_length=750,
                n=10)

    def test_compare_with_excess_resource(self):

        fuzzi_moss.fuzz.enable_fuzzings = False

        self.waterfall_projects.build_and_operate()
        self.tdd_projects.build_and_operate()

        self.print_output()

    def test_compare_with_fuzzing(self):

        fuzzi_moss.fuzz.enable_fuzzings = True

        self.waterfall_projects.build_and_operate()
        self.tdd_projects.build_and_operate()

        self.print_output()

    def print_output(self):

        def create_result_row(workflow_label, projects_group):
            return ",\t".join([workflow_label,
                               str(projects_group.average_project_mean_time_to_failure),
                               str(projects_group.average_project_remaining_developer_time),
                               str(projects_group.average_project_features_implemented)])

        print "Work flow,\tMTF,\tRDT,CP"
        print create_result_row("Waterfall", self.waterfall_projects)
        print create_result_row("TDD", self.tdd_projects)


if __name__ == '__main__':
    unittest.main()
