"""
@author tws
"""
from theatre_ag import Actor

from ..workflows.test_driven_development import TestDrivenDevelopment


class TDDDeveloper(Actor):

    def __init__(self, name, clock, centralised_vcs_server):
        Actor.__init__(self, name, clock)
        self.test_driven_development = TestDrivenDevelopment(self, centralised_vcs_server)


class TDDDevelopmentTeam(object):

    def __init__(self, developers=list()):
        self.developers = developers

    def add_developer(self, developer):
        self.developers.add(developer)

    def build_software_system(self, product_backlog):
        for developer in self.developers:
            developer.allocate_task(developer.test_driven_development.work_from_backlog, [product_backlog])

        for developer in self.developers:
            developer.start()

        for developer in self.developers:
            developer.shutdown()