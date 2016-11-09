"""
@author tws
"""

from ..workflows.test_driven_development import TestDrivenDevelopment
from ..workflows.waterfall import Waterfall


class DevelopmentPlan(object):

    def __init__(self, centralised_vcs_server, random):
        self.centralised_vcs_server = centralised_vcs_server
        self.random = random

    @property
    def release(self):
        return self.centralised_vcs_server.checkout().working_copy

    def apply(self, team):
        raise NotImplemented("not implemented")


class WaterfallDevelopmentPlan(DevelopmentPlan):

    def __init__(self, centralised_vcs_server, specification, random):
        super(WaterfallDevelopmentPlan, self).__init__(centralised_vcs_server, random)
        self.specification = specification

    def apply(self, team):

        team_manager = team.team_members[0]

        waterfall_task = Waterfall(team.team_members, self.centralised_vcs_server)

        team_manager.allocate_task(
            waterfall_task, waterfall_task.allocate_tasks, [self.specification, self.random])


class TestDrivenDevelopmentPlan(DevelopmentPlan):

    def __init__(self, centralised_vcs_server, product_backlog, random):
        super(TestDrivenDevelopment, self).__init__(centralised_vcs_server, random)
        self.product_backlog = product_backlog

    def apply(self, team):
        for developer in team.team_members:
            tdd_task = TestDrivenDevelopment(self.centralised_vcs_server)
            developer.allocate_task(tdd_task, tdd_task.work_from_backlog, [self.product_backlog, self.random])

