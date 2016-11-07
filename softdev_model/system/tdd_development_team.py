"""
@author tws
"""
from theatre_ag import Actor

from ..workflows.test_driven_development import TestDrivenDevelopment


class TDDDevelopmentTeam(object):

    def __init__(self, clock, centralised_vcs_server):
        self.clock = clock
        self.centralised_vcs_server = centralised_vcs_server

        self.developers = list()

    def add_developer(self, logical_name):
        actor = Actor(logical_name, self.clock)
        self.developers.append(actor)

    def build_software_system(self, product_backlog, random):
        for developer in self.developers:
            tdd_task = TestDrivenDevelopment(developer, self.centralised_vcs_server)
            developer.allocate_task(tdd_task, tdd_task.work_from_backlog, [product_backlog, random])

        for developer in self.developers:
            developer.start()

        for developer in self.developers:
            developer.shutdown()

    @property
    def release(self):
        return self.centralised_vcs_server.checkout().working_copy

