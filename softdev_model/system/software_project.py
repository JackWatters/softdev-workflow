"""
@author twsswt
@author probablytom
"""

from .bug import BugEncounteredException
from .feature import InoperableFeatureException


class SoftwareProject(object):
    """
    Represents the overall state and behaviour of a software project.
    """

    def __init__(self, clock, development_team, plan, centralised_vcs_server, random):

        self.random = random
        self.clock = clock
        self.development_team = development_team
        self.plan = plan
        self.centralised_vcs_server = centralised_vcs_server

        self.deployments = list()

    def build(self):
        self.plan.apply(self.development_team, self.centralised_vcs_server)
        self.clock.start()
        self.development_team.start()
        self.clock.wait_for_last_tick()

    def deploy_and_operate(self, number_of_traces, max_trace_length):
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
        return self.development_team.last_tick

    def task_count(self, task_spec=None):
        return self.development_team.task_count(task_spec)


