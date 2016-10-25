from theatre_ag import workflow

from softdev_model.system import BugEncounteredException

from .change_management import ChangeManagement


class Debugging(ChangeManagement, object):

    @workflow(1)
    def debug(self, feature, bug, random):
        feature.debug(random, bug)

    @workflow()
    def debug_test(self, test, random):
        while True:
            try:
                test.exercise()
                break
            except BugEncounteredException as e:
                self.debug(test.feature, e.bug, random)
                self.commit_changes(random)

    @workflow()
    def debug_feature(self, feature, random):
        for test in feature.tests:
            self.debug_test(test, random)

    @workflow()
    def debug_system(self, random):
        self.checkout()
        for test in self.centralised_vcs_client.working_copy.tests:
            self.debug_test(test, random)
