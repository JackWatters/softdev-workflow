import unittest

from softdev_model.system.software.bug import Bug
from softdev_model.system.software.chunk import Chunk
from softdev_model.system.software.feature import Feature
from softdev_model.system.software.software_project import SoftwareProject
from softdev_model.system.software.test import Test
from softdev_model.workflows.test_driven_development import TestDrivenDevelopment
from softdev_model.workflows.waterfall import Waterfall


class TestCompareWorkFlows(unittest.TestCase):

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.waterfall_projects =\
            [SoftwareProject.create_software_project(i, Waterfall,             250, [3, 5, 7], 50) for i in range(0, 10)]
        self.tdd_projects =\
            [SoftwareProject.create_software_project(i, TestDrivenDevelopment, 250, [3, 5, 7], 50) for i in range(0, 10)]

    @staticmethod
    def build_software_systems(projects):
        for project in projects:
            project.build_and_operate()

        print reduce(lambda x, y: x + y, map(lambda p: p.software_system.mean_operations_to_failure, projects), 0)
        print reduce(lambda x, y: x + y, map(lambda p: p.developer.person_time, projects), 0)

    def test_compare_with_excess_resource(self):
        print "Waterfall"
        self.build_software_systems(self.waterfall_projects)
        print "TDD"
        self.build_software_systems(self.tdd_projects)

if __name__ == '__main__':
    unittest.main()
