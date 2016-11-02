from theatre_ag import default_cost, Workflow


class Implementation(Workflow):

    def __init__(self, actor, change_management):
        super(Implementation, self).__init__(actor)
        self.change_management = change_management

    @default_cost(1)
    def add_chunk(self, chunk_logical_name, feature, random):
        feature.extend(chunk_logical_name, random)

    @default_cost()
    def implement_feature(self, feature, random):
        chunk_count = 0
        while not feature.is_implemented:
            self.add_chunk(chunk_count, feature, random)
            chunk_count += 1
            self.change_management.commit_changes(random)

    @default_cost()
    def implement_system(self, random):

        self.change_management.checkout()

        for feature in self.change_management.centralised_vcs_client.working_copy.features:
            self.implement_feature(feature, random)
