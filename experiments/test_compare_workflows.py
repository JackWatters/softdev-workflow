import unittest

import fuzzi_moss

from random import Random

from softdev_model.system import Bug, Chunk, Developer, Feature, SoftwareProject, SoftwareSystem, Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall


class TestCompareWorkFlows(unittest.TestCase):
    fuzzi_moss.fuzz.enable_fuzzings = False

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        def create_software_projects(workflow):
            return [SoftwareProject(
                random=Random(seed),
                software_system=SoftwareSystem(),
                workflow=workflow,
                developer=Developer(person_time=250),
                schedule=[3, 5, 7],
                number_of_traces=50,
                max_trace_length=750) for seed in range(0, 10)]

        self.waterfall_projects = create_software_projects(Waterfall)
        self.tdd_projects = create_software_projects(TestDrivenDevelopment)

    def test_compare_with_excess_resource(self):
        for project in self.waterfall_projects + self.tdd_projects:
            project.build_and_operate()

        print "Work flow,\tMTF,\tRDT"
        print TestCompareWorkFlows.create_result_row("Waterfall", self.waterfall_projects)
        print TestCompareWorkFlows.create_result_row("TDD", self.tdd_projects)

    @staticmethod
    def average_project_attribute(projects, attr):
        return reduce(lambda x, y: x + y, map(attr, projects), 0) / len(projects)

    @staticmethod
    def average_project_mean_time_to_failure(projects):
        return TestCompareWorkFlows. \
            average_project_attribute(projects, lambda p: p.software_system.mean_operations_to_failure)

    @staticmethod
    def average_project_remaining_developer_time(projects):
        return TestCompareWorkFlows. \
            average_project_attribute(projects, lambda p: p.developer.person_time)

    @staticmethod
    def create_result_row(workflow_label, projects):
        return ",\t".join([workflow_label,
                           str(TestCompareWorkFlows.average_project_mean_time_to_failure(projects)),
                           str(TestCompareWorkFlows.average_project_remaining_developer_time(projects))])


if __name__ == '__main__':
    unittest.main()
