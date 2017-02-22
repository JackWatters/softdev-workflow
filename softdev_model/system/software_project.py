"""
@author twsswt
@author probablytom
"""

from .bug import BugEncounteredException
from .feature import InoperableFeatureException

from theatre_ag import Episode


class SoftwareProject(Episode):
    """
    Represents the overall state and behaviour of a software project.
    """

    def __init__(self, clock, development_team, plan, random):
        super(SoftwareProject, self).__init__(clock, development_team, directions=plan)

        self.random = random

        self.deployments = list()

    def deploy_and_operate(self, number_of_traces, max_trace_length):
        deployment = self.directions.centralised_vcs_server.checkout().working_copy
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
        return self.cast.last_tick

    def task_count(self, task_spec=None):
        return self.cast.task_count(task_spec)


