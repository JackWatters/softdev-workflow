from theatre_ag import default_cost

from softdev_model.system import BugEncounteredException

from .change_management import commit_changes


@default_cost(1)
def debug(self, feature, bug, random):
    feature.debug(random, bug)


def debug_test(self, test, centralised_vcs_client, random):
    while True:
        try:
            test.exercise()
            break
        except BugEncounteredException as e:
            self.perform_task(debug, [test.feature, e.bug, random])
            self.perform_task(commit_changes, [centralised_vcs_client, random])


def debug_feature(self, centralised_vcs_client, feature, random):
    for test in feature.tests:
        self.perform_task(debug_test, [test, centralised_vcs_client, random])


def debug_system(self, centralised_vcs_client, random):
    for test in centralised_vcs_client.working_copy.tests:
        self.perform_task(debug_test, [test, centralised_vcs_client, random])
