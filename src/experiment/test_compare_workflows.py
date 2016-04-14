import unittest

from models.systems.software.bug import Bug
from models.systems.software.chunk import Chunk
from models.systems.software.feature import Feature
from models.systems.software.software_project import SoftwareProject
from models.systems.software.test import Test

from models.workflows.test_driven_development import TestDrivenDevelopment
from models.workflows.waterfall import Waterfall


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
