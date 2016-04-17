"""
@author twsswt
@author probablytom
"""

from .bug import BugEncounteredException
from .developer import DeveloperExhaustedException
from .feature import InoperableFeatureException


class SoftwareProject(object):
    """
    Represents the overall state and behaviour of a software project.
    """
    def __init__(self, random, software_system, workflow, developer, schedule, number_of_traces, max_trace_length):
        self.random = random
        self.software_system = software_system
        self.workflow = workflow
        self.developer = developer
        self.schedule = schedule
        self.number_of_traces = number_of_traces
        self.max_trace_length = max_trace_length

    def build_and_operate(self):
        try:
            self.workflow.work(self.random, self.developer, self.schedule)
        except DeveloperExhaustedException:
            pass
        for _ in range(0, self.number_of_traces):
            try:
                self.software_system.operate(self.random, self.max_trace_length)
            except BugEncounteredException or InoperableFeatureException:
                pass
