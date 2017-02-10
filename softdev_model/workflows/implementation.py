from theatre_ag import default_cost


class Implementation(object):

    is_workflow = True

    def __init__(self, change_management):
        self.change_management = change_management

    @default_cost(1)
    def add_chunk(self, chunk_logical_name, feature, random):
        feature.extend(chunk_logical_name, random)

    @default_cost()
    def implement_feature(self, logical_name, random):

        self.change_management.checkout()

        feature = self.change_management.centralised_vcs_client.working_copy.get_feature(logical_name)

        while not feature.is_implemented:
            self.add_chunk(len(feature.chunks), feature, random)
            self.change_management.commit_changes(random)

    @default_cost()
    def implement_system(self, random):

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self.implement_feature(feature, random)
