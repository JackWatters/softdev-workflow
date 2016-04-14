import unittest

from models.systems.software.bug import Bug, BugEncounteredException
from models.systems.software.chunk import Chunk
from models.systems.software.developer import Developer, DeveloperExhaustedException
from models.systems.software.feature import Feature, InoperableFeatureException
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.test import Test

from models.workflows.test_driven_development import TestDrivenDevelopment
from models.workflows.waterfall import Waterfall

from random import Random


class SoftwareProject(object):

    def __init__(self, random, software_system, workflow, developer, schedule, operations):
        self.random = random
        self.software_system = software_system
        self.workflow = workflow
        self.developer = developer
        self.schedule = schedule
        self.operations = operations

    def build_and_operate(self):
        try:
            self.workflow.work(self.random, self.developer, self.schedule)
        except DeveloperExhaustedException:
            pass
        for _ in range(0, self.operations):
            try:
                self.software_system.operate(self.random, 750)
            except BugEncounteredException or InoperableFeatureException:
                pass


class TestCompareWorkFlows(unittest.TestCase):

    @staticmethod
    def create_software_project(seed, workflow_constructor, resources, schedule, operations):
        developer = Developer(resources)
        software_system = SoftwareSystem()
        workflow = workflow_constructor(software_system)
        random = Random(seed)
        return SoftwareProject(random, software_system, workflow, developer, schedule, operations)

    def setUp(self):
        Chunk._count = 0
        Feature._count = 0
        Test._count = 0
        Bug._count = 0

        self.waterfall_projects =\
            [self.create_software_project(i, Waterfall,             250, [3, 5, 7], 50) for i in range(0, 10)]
        self.tdd_projects =\
            [self.create_software_project(i, TestDrivenDevelopment, 250, [3, 5, 7], 50) for i in range(0, 10)]

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
