"""
@author twsswt
@author probablytom
"""

import time

from theatre_ag import SynchronizingClock, Team

from .bug import BugEncounteredException
from .feature import InoperableFeatureException
from .system_random import SystemRandom

from .centralised_vcs import CentralisedVCSServer
from .software_system import SoftwareSystem


class SoftwareProject(object):
    """
    Represents the overall state and behaviour of a software project.
    """

    def __init__(self,
                 random,
                 clock,
                 development_team,
                 plan,
                 centralised_vcs_server,
                 number_of_traces,
                 max_trace_length):

        self.random = random
        self.clock = clock
        self.development_team = development_team
        self.plan = plan
        self.centralised_vcs_server = centralised_vcs_server
        self.number_of_traces = number_of_traces
        self.max_trace_length = max_trace_length

    def build_and_operate(self):
        self.plan.apply(self.development_team, self.centralised_vcs_server)
        self.clock.start()
        self.development_team.perform()
        self.clock.shutdown()

        for _ in range(0, self.number_of_traces):
            try:
                self.release.operate(self.random, self.max_trace_length)
            except (BugEncounteredException, InoperableFeatureException):
                pass

    @property
    def release(self):
        return self.centralised_vcs_server.checkout().working_copy


    @property
    def project_duration(self):
        # TODO
        return 0


class SoftwareProjectGroup(object):

    def __init__(self, plan, number_of_developers, number_of_clock_ticks, number_of_traces, max_trace_length, n):
        self.software_projects = list()

        for seed in range(0, n):

            clock = SynchronizingClock(number_of_clock_ticks)

            development_team = Team(clock)

            for logical_name in range(0, number_of_developers):
                development_team.add_member(logical_name)

            centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

            software_project = SoftwareProject(
                SystemRandom(seed),
                clock,
                development_team,
                plan,
                centralised_vcs_server,
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
        return self._average_project_attribute(lambda p: p.release.mean_operations_to_failure)

    @property
    def average_project_remaining_developer_time(self):
        return self._average_project_attribute(lambda p: p.project_duration)

    @property
    def average_project_features_implemented(self):
        return self._average_project_attribute(lambda p: 1.0 * len(p.release.features))
