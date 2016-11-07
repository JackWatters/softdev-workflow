"""
@author tws
"""
from theatre_ag import Actor, Team

from ..workflows.test_driven_development import TestDrivenDevelopment


class TDDDevelopmentTeam(Team):

    def __init__(self, clock, centralised_vcs_server, product_backlog, random):
        super(TDDDevelopmentTeam, self).__init__(clock)
        self.centralised_vcs_server = centralised_vcs_server
        self.product_backlog = product_backlog
        self.random = random

    def allocate_tasks(self):
        for developer in self.team_members:
            tdd_task = TestDrivenDevelopment(developer, self.centralised_vcs_server)
            developer.allocate_task(tdd_task, tdd_task.work_from_backlog, [self.product_backlog, self.random])

    @property
    def release(self):
        return self.centralised_vcs_server.checkout().working_copy

