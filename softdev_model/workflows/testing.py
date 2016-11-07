from theatre_ag import default_cost, Workflow


class Testing(Workflow):

    def __init__(self, actor, change_management, target_test_coverage_per_feature=1.0, target_tests_per_chunk_ratio=1):
        super(Testing, self).__init__(actor)
        self.change_management = change_management
        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_tests_per_chunk_ratio = target_tests_per_chunk_ratio

    @default_cost(1)
    def add_test(self, logical_name, feature):
        feature.add_test(logical_name)

    @default_cost()
    def test_per_chunk_ratio(self, feature_logical_name, random):

        self.change_management.checkout()

        feature = self.change_management.centralised_vcs_client.working_copy.get_feature(feature_logical_name)

        test_count = 0

        while feature.test_coverage < self.target_test_coverage_per_feature or \
                feature.tests_per_chunk_ratio < self.target_tests_per_chunk_ratio:

            self.add_test(test_count, feature)
            test_count += 1
            self.change_management.commit_changes(random)

    @default_cost()
    def complete_system_test_suite(self, random):

        self.change_mangement.checkout()

        for feature in self.centralised_vcs_client.working_copy.features:
            self.test_per_chunk_ratio(feature, random)
