from theatre_ag import default_cost


class Specification(object):

    is_workflow = True

    def __init__(self, change_management):
        self.change_management = change_management

    @default_cost(1)
    def add_feature(self, logical_name, size, random):
        self.change_management.checkout()
        self.change_management.centralised_vcs_client.working_copy.add_feature(logical_name, size)
        self.change_management.commit_changes(random)

    @default_cost()
    def complete_specification(self, schedule, random):
        for logical_name, feature_size in schedule:
            self.add_feature(logical_name, feature_size, random)

