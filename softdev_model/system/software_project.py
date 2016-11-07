"""
@author twsswt
@author probablytom
"""

import time

from theatre_ag import SynchronizingClock

from .bug import BugEncounteredException
from .centralised_vcs import CentralisedVCSServer
from .feature import InoperableFeatureException
from .software_system import SoftwareSystem
from .tdd_development_team import TDDDevelopmentTeam

from random import Random


class SoftwareProject(object):
    """
    Represents the overall state and behaviour of a software project.
    """

    def __init__(self,
                 random,
                 development_team,
                 schedule,
                 number_of_traces,
                 max_trace_length):

        self.random = random
        self.development_team = development_team
        self.schedule = schedule
        self.number_of_traces = number_of_traces
        self.max_trace_length = max_trace_length

    def build_and_operate(self):
        self.development_team.perform()

        for _ in range(0, self.number_of_traces):
            try:
                self.software_system.operate(self.random, self.max_trace_length)
            except (BugEncounteredException, InoperableFeatureException):
                pass

    @property
    def software_system(self):
        return self.development_team.release


class SoftwareProjectGroup(object):

    def __init__(self, schedule, number_of_developers, number_of_traces, max_trace_length, n):
        self.software_projects = list()

        for seed in range(0, n):

            development_team = TDDDevelopmentTeam(SynchronizingClock(), CentralisedVCSServer(SoftwareSystem()))

            for logical_name in range(0, number_of_developers):
                development_team.add_developer(logical_name)

            software_project = SoftwareProject(
                Random(seed),
                development_team,
                schedule,
                number_of_traces,
                max_trace_length)

            self.software_projects.append(software_project)

        self.duration = -1

    def build_and_operate(self):
        start_time = time.time()
        for software_project in self.software_projects:
            software_project.build_and_operate()
        self.duration = time.time() - start_time

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
