"""
@author tws
"""
from theatre_ag import Actor

from .test_driven_development import TestDrivenDevelopment


class TDDDeveloper(TestDrivenDevelopment, Actor):

    def __init__(self, name, clock, centralised_vcs_server):
        Actor.__init__(self, name, clock)
        TestDrivenDevelopment.__init__(self, centralised_vcs_server)
