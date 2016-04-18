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
    def __init__(self, random, software_system, workflow, developer, schedule, number_of_traces, max_trace_length):
        self.random = random
        self.software_system = software_system
        self.workflow = workflow
        self.developer = developer
        self.schedule = schedule
        self.number_of_traces = number_of_traces
        self.max_trace_length = max_trace_length

    def build_and_operate(self):
        try:
            self.workflow.work(self.random, self.software_system, self.developer, self.schedule)
        except DeveloperExhaustedException:
            pass
        for _ in range(0, self.number_of_traces):
            try:
                self.software_system.operate(self.random, self.max_trace_length)
            except BugEncounteredException or InoperableFeatureException:
                pass


class SoftwareProjectGroup(object):

    def __init__(self, workflow, person_time, schedule, number_of_traces, max_trace_length, n):
        self.software_projects = list()

        for seed in range (0, n):
            software_project = SoftwareProject(
                random=Random(seed),
                software_system=SoftwareSystem(),
                workflow=workflow(),
                developer=Developer(person_time),
                schedule=schedule,
                number_of_traces=number_of_traces,
                max_trace_length=max_trace_length)

            self.software_projects.append(software_project)

    def build_and_operate(self):
        for software_project in self.software_projects:
            software_project.build_and_operate()

    def _average_project_attribute(self, attr):
        return reduce(lambda x, y: x + y, map(attr, self.software_projects), 0) / len(self.software_projects)

    @property
    def average_project_mean_time_to_failure(self):
        return self._average_project_attribute(lambda p: p.software_system.mean_operations_to_failure)

    @property
    def average_project_remaining_developer_time(self):
        return self._average_project_attribute(lambda p: p.developer.person_time)

    @property
    def average_project_features_implemented(self):
        return self._average_project_attribute(lambda p: 1.0 * len(p.software_system.features))