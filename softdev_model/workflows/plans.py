"""
@author tws
"""

from .test_driven_development import TestDrivenDevelopment
from .waterfall import Waterfall

from Queue import Queue


class WaterfallDevelopmentPlan(object):

    def __init__(self, specification, centralised_vcs_server, random):
        self.specification = specification
        self.centralised_vcs_server = centralised_vcs_server
        self.random = random

    def apply(self, team):

        waterfall_task = Waterfall(team, self.centralised_vcs_server)

        list(team)[0].allocate_task(
            waterfall_task.allocate_tasks, waterfall_task, [self.specification, self.random])


class TestDrivenDevelopmentPlan(object):

    def __init__(self, specification, centralised_vcs_server, random):
        self.specification = specification
        self.centralised_vcs_server = centralised_vcs_server
        self.random = random

    def apply(self, team):

        product_backlog = Queue()
        for user_story in self.specification:
            product_backlog.put(user_story)

        for developer in team:
            tdd_task = TestDrivenDevelopment(self.centralised_vcs_server)
            developer.allocate_task(tdd_task.work_from_backlog, tdd_task, [product_backlog, self.random])
