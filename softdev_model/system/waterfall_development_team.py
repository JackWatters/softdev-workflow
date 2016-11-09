"""
@author tws
"""
from theatre_ag import Actor, Team

from ..workflows.waterfall import Waterfall


class WaterfallDevelopmentTeam(Team):

    def __init__(self, clock, centralised_vcs_server, specification, random):
        super(WaterfallDevelopmentTeam, self).__init__(clock)
        self.centralised_vcs_server = centralised_vcs_server
        self.specification = specification
        self.random = random

    def allocate_tasks(self):

        team_manager = self.team_members[0]

        waterfall_task = Waterfall(self.team_members, self.centralised_vcs_server)

        team_manager.allocate_task(
            waterfall_task, waterfall_task.allocate_tasks, [self.specification, self.random])

    @property
    def release(self):
        return self.centralised_vcs_server.checkout().working_copy

