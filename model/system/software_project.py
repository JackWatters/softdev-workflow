"""
@author twsswt
@author probablytom
"""

from .bug import BugEncounteredException
from .developer import Developer, DeveloperExhaustedException
from .feature import InoperableFeatureException
from .software_system import SoftwareSystem

from random import Random


class SoftwareProject(object):
    """
    Represents the overall state and behaviour of a software project.
    """
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

    @staticmethod
    def create_software_project(seed, workflow_constructor, resources, schedule, operations):
        developer = Developer(resources)
        software_system = SoftwareSystem()
        workflow = workflow_constructor(software_system)
        random = Random(seed)
        return SoftwareProject(random, software_system, workflow, developer, schedule, operations)

