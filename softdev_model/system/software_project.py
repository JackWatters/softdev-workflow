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
                 centralised_vcs_server):

        self.random = random
        self.clock = clock
        self.development_team = development_team
        self.plan = plan
        self.centralised_vcs_server = centralised_vcs_server

        self.deployments = list()

    def build(self):
        self.plan.apply(self.development_team, self.centralised_vcs_server)
        self.clock.start()
        self.development_team.perform()
        self.clock.shutdown()

    def deploy_and_operate(self, number_of_traces, max_trace_length ):
        deployment = self.centralised_vcs_server.checkout().working_copy
        self.deployments.append(deployment)

        for _ in range(0, number_of_traces):
            try:
                deployment.operate(self.random, max_trace_length)
            except (BugEncounteredException, InoperableFeatureException):
                pass

    @property
    def last_deployment(self):
        index = len(self.deployments) - 1
        return None if index < 0 else self.deployments[index]

    @property
    def project_duration(self):

        finish_ticks = \
            map(lambda d: 0 if d.last_completed_task is None else d.last_completed_task.finish_tick,
                self.development_team.team_members)

        reduce(min, finish_ticks)

        return self.clock.current_tick


class SoftwareProjectGroup(object):

    def __init__(self, plan, number_of_developers, number_of_clock_ticks, number_of_traces, max_trace_length, n):

        self.number_of_traces =number_of_traces
        self.max_trace_length = max_trace_length

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
                centralised_vcs_server)

            self.software_projects.append(software_project)

        self.duration = -1

    def build_and_operate(self):
        start_time = time.time()
        for software_project in self.software_projects:
            software_project.build()
            software_project.deploy_and_operate(self.number_of_traces,  self.max_trace_length)

        self.duration = time.time() - start_time

    def _average_project_attribute(self, attr):
        return reduce(lambda x, y: x + y, map(attr, self.software_projects), 0) / len(self.software_projects)

    @property
    def average_project_mean_time_to_failure(self):
        return self._average_project_attribute(lambda p: p.last_deployment.mean_operations_to_failure)

    @property
    def average_project_remaining_developer_time(self):
        return self._average_project_attribute(lambda p: p.project_duration)

    @property
    def average_project_features_implemented(self):
        return self._average_project_attribute(lambda p: 1.0 * len(p.last_deployment.features))
