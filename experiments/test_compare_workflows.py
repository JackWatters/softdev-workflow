import unittest

from nose_parameterized import parameterized

import pydysofu

import fuzzi_moss

from fuzzi_moss import incomplete_procedure, default_incomplete_procedure_pmf

from softdev_model.system import SoftwareProjectGroup, SystemRandom, UserStory

from softdev_model.workflows import ChangeManagement, Debugging, Implementation, Refactoring, \
    Specification, Testing, TestDrivenDevelopment, TestDrivenDevelopmentPlan, Waterfall, WaterfallDevelopmentPlan


random = SystemRandom(1)

specification = [UserStory(0, 3, 1), UserStory(1, 5, 2), UserStory(2, 7, 3)]


def create_experimental_parameters():
    return [
        (plan, team_size, max_clock_tick, concentration, fuzz_classes)
        for fuzz_classes in [
            [ChangeManagement, Specification, Testing, Implementation, Debugging, Refactoring],
            [Waterfall, TestDrivenDevelopment],
            [ChangeManagement, Specification, Testing, Implementation, Debugging, Refactoring, Waterfall,
             TestDrivenDevelopment]
        ]
        for plan in [WaterfallDevelopmentPlan, TestDrivenDevelopmentPlan]
        for team_size in [2, 4]
        for max_clock_tick in [150, 300, 450]
        for concentration in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    ]


def test_name_func(func, param_num, param):
    return "%s_%03d" % (func.__name__, param_num)


class TestCompareWorkFlows(unittest.TestCase):

    def setUp(self):
        pydysofu.pydysofu_random.seed(1)

    headers_printed = False

    @staticmethod
    def print_data_row(data_format_tuples):

        if not TestCompareWorkFlows.headers_printed:
            headers = map(lambda t: t[0], data_format_tuples)
            print ", ".join(map(lambda h: h.rjust(10, ' '), headers))
            TestCompareWorkFlows.headers_printed = True

        row_format_string = ", ".join(map(lambda t: t[1], data_format_tuples))
        data = map(lambda t: t[2], data_format_tuples)

        print row_format_string % tuple(data)

    @parameterized.expand(create_experimental_parameters, testcase_func_name=test_name_func)
    def test_compare_workflows(self, plan, team_size, max_clock_tick, concentration, fuzz_classes):

        workflow_advice = {
            ChangeManagement.commit_changes:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Specification.add_feature:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Implementation.implement_feature:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Testing.test_per_chunk_ratio:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Debugging.debug_feature:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Refactoring.refactor_feature:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            TestDrivenDevelopment.implement_feature_tdd:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration)),
            Waterfall.allocate_tasks:
                incomplete_procedure(random, pmf=default_incomplete_procedure_pmf(concentration))
        }

        for clazz in fuzz_classes:
            pydysofu.fuzz_clazz(clazz, workflow_advice)

        projects_group = SoftwareProjectGroup(specification, plan, team_size, max_clock_tick,
                                              number_of_projects=20,
                                              number_of_traces=10,
                                              max_trace_length=750,
                                              random=random)

        projects_group.build_and_operate()

        data_format_tuples = (
            # Preamble
            ("workflow", "%-10s", plan.__name__[0:10]),
            ("t_alloc", "%10d", max_clock_tick),
            ("#team", "%10d", team_size),

            # Fuzz parameters
            ("fuzzed", "%-10s", reduce(lambda a, b: a+b, map(lambda c: c.__name__[0], fuzz_classes), "")),
            ("co", "%10.3f", concentration),

            # Task counts
            ("#exec_wf", "%10d", projects_group.task_count(Waterfall.allocate_tasks)),
            ("#exec_tdd", "%10d", projects_group.task_count(TestDrivenDevelopment.implement_feature_tdd)),
            ("#exec_co", "%10d", projects_group.task_count(ChangeManagement.commit_changes)),
            ("#exec_spc", "%10d", projects_group.task_count(Specification.add_feature)),
            ("#exec_imp", "%10d", projects_group.task_count(Implementation.add_chunk)),
            ("#exec_tng", "%10d", projects_group.task_count(Testing.test_per_chunk_ratio)),
            ("#exec_dbg", "%10d", projects_group.task_count(Debugging.debug_feature)),
            ("#exec_rfg", "%10d", projects_group.task_count(Refactoring.refactor_feature)),

            # Fuzz counts
            ("#fuzz_wf", "%10d",  fuzzi_moss.lines_removed_count(Waterfall)),
            ("#fuzz_tdd", "%10d",  fuzzi_moss.lines_removed_count(TestDrivenDevelopment)),
            ("#fuzz_co", "%10d",  fuzzi_moss.lines_removed_count(ChangeManagement)),
            ("#fuzz_spc", "%10d", fuzzi_moss.lines_removed_count(Specification)),
            ("#fuzz_imp", "%10d", fuzzi_moss.lines_removed_count(Implementation)),
            ("#fuzz_tng", "%10d", fuzzi_moss.lines_removed_count(Testing)),
            ("#fuzz_dbg", "%10d", fuzzi_moss.lines_removed_count(Debugging)),
            ("#fuzz_rfg", "%10d", fuzzi_moss.lines_removed_count(Refactoring)),
            ("#fuzz_tot", "%10d", fuzzi_moss.lines_removed_count()),

            ("#lines_wf", "%10d", fuzzi_moss.removable_lines_count(Waterfall.allocate_tasks)),
            ("#lines_tdd", "%10d", fuzzi_moss.removable_lines_count(TestDrivenDevelopment.implement_feature_tdd)),
            ("#lines_co", "%10d", fuzzi_moss.removable_lines_count(ChangeManagement.commit_changes)),
            ("#lines_spc", "%10d", fuzzi_moss.removable_lines_count(Specification.add_feature)),
            ("#lines_imp", "%10d", fuzzi_moss.removable_lines_count(Implementation.add_chunk)),
            ("#lines_tng", "%10d", fuzzi_moss.removable_lines_count(Testing.test_per_chunk_ratio)),
            ("#lines_dbg", "%10d", fuzzi_moss.removable_lines_count(Debugging.debug_feature)),
            ("#lines_rfg", "%10d", fuzzi_moss.removable_lines_count(Refactoring.refactor_feature)),

            # Project characteristics
            ("mtf", "%10.2f", projects_group.average_project_mean_time_to_failure),
            ("t_used", "%10d", projects_group.average_project_time_used),
            ("#ftrs", "%10.2f", projects_group.average_project_features_implemented),
            ("#t_run", "%10d", projects_group.simulation_duration)
        )

        self.print_data_row(data_format_tuples)

        pydysofu.reset_invocation_counters()
        fuzzi_moss.reset_lines_removed_counters()

        pydysofu.defuzz_all_classes()

if __name__ == '__main__':
    unittest.main()
