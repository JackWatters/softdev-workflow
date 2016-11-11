"""
@author tws
"""

from ..workflows.test_driven_development import TestDrivenDevelopment
from ..workflows.waterfall import Waterfall


class DevelopmentPlan(object):

    def __init__(self, random):
        self.random = random

    def apply(self, team, centralised_vcs_server):
        raise NotImplemented("not implemented")


class WaterfallDevelopmentPlan(DevelopmentPlan):

    def __init__(self, specification, random):
        super(WaterfallDevelopmentPlan, self).__init__(random)
        self.specification = specification

    def apply(self, team, centralised_vcs_server):

        team_manager = team.team_members[0]

        waterfall_task = Waterfall(team.team_members, centralised_vcs_server)

        team_manager.allocate_task(
            waterfall_task, waterfall_task.allocate_tasks, [self.specification, self.random])


class TestDrivenDevelopmentPlan(DevelopmentPlan):

    def __init__(self, product_backlog, random):
        super(TestDrivenDevelopmentPlan, self).__init__(random)
        self.product_backlog = product_backlog

    def apply(self, team, centralised_vcs_server):
        for developer in team.team_members:
            tdd_task = TestDrivenDevelopment(centralised_vcs_server)
            developer.allocate_task(tdd_task, tdd_task.work_from_backlog, [self.product_backlog, self.random])

