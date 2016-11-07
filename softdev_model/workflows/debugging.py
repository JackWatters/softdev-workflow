from theatre_ag import default_cost, Workflow

from softdev_model.system import BugEncounteredException


class Debugging(Workflow):

    def __init__(self, actor, change_management):
        super(Debugging, self).__init__(actor)
        self.change_management = change_management

    @default_cost(1)
    def debug(self, feature, bug, random):
        feature.debug(random, bug)

    @default_cost()
    def debug_test(self, test, random):
        while True:
            try:
                test.exercise()
                break
            except BugEncounteredException as e:
                self.debug(test.feature, e.bug, random)
                self.change_management.commit_changes(random)

    @default_cost()
    def debug_feature(self, logical_name, random):

        self.change_management.checkout()

        feature = self.change_management.centralised_vcs_client.working_copy.get_feature(logical_name)

        for test in feature.tests:
            self.debug_test(test, random)

    @default_cost()
    def debug_system(self, random):
        self.change_management.checkout()
        for test in self.change_management.centralised_vcs_client.working_copy.tests:
            self.debug_test(test, random)
