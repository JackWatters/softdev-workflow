from softdev_model.system import SoftwareProjectGroup, SystemRandom, UserStory

from softdev_model.workflows import ChangeManagement, Debugging, Implementation, Refactoring, \
    Specification, Testing, TestDrivenDevelopment, TestDrivenDevelopmentPlan, Waterfall, WaterfallDevelopmentPlan


headers_printed = False


def format_headers(header_format_data_tuples):
    headers = map(lambda t: t[0], header_format_data_tuples)
    return ", ".join(map(lambda h: h.rjust(10, ' '), headers))


def format_row(header_format_data_tuples):
    row_format_string = ", ".join(map(lambda t: t[1], header_format_data_tuples))
    data = map(lambda t: t[2], header_format_data_tuples)
    return row_format_string % tuple(data)


results_file = open('./data.csv', 'w')

user_stories = [
        UserStory(0, 2),
        UserStory(1, 2),
        UserStory(2, 2),
        UserStory(3, 2),
        UserStory(4, 2),
        UserStory(5, 2),
        UserStory(6, 4),
        UserStory(7, 4),
        UserStory(8, 4),
        UserStory(9, 4),
        UserStory(10, 4),
        UserStory(11, 4),
]

experimental_parameters = [
        (fuzz_classes, plan, team_size, user_story_indexes, max_clock_tick, concentration)
        for plan in [WaterfallDevelopmentPlan, TestDrivenDevelopmentPlan]
        for fuzz_classes in [
            [ChangeManagement, Testing, Implementation, Debugging, Refactoring],
            [Waterfall, TestDrivenDevelopment],
        ]
        for team_size in [3]
        for max_clock_tick in [500]
        for user_story_indexes in [
            [0],
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 3],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4, 5],
            [6],
            [6, 7],
            [6, 7, 8],
            [6, 7, 8, 9],
            [6, 7, 8, 9, 10],
            [6, 7, 8, 9, 10, 11]
        ]
        for concentration in [
            0.001,
            0.002,
            0.005,
            0.01,
            0.02,
            0.05,
            0.1,
            0.2,
            0.5,
            1.0,
            5.0
        ]
    ]

print ("Running" , len(experimental_parameters), " experiments.")

for fuzz_classes, plan, team_size, user_story_indexes, max_clock_tick, concentration in experimental_parameters:

    configuration_format = (
        ("workflow", "%-10s", plan.__name__[0:10]),
        ("t_alloc", "%10d", max_clock_tick),
        ("#team", "%10d", team_size),
        ("#ftrs_spec", "%10s", " ".join(map(lambda i: str(i), user_story_indexes))),
        ("fuzzed", "%-10s", reduce(lambda a, b: a + b, map(lambda c: c.__name__[0], fuzz_classes), "")),
        ("co", "%10.3f", concentration),
    )

    print ("Executing", format_row(configuration_format))

    random = SystemRandom(1)
    pydysofu.pydysofu_random.seed(1)

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

    project_user_stories = [user_stories[user_story_index] for user_story_index in user_story_indexes]

    projects_group = SoftwareProjectGroup(project_user_stories,
                                          plan,
                                          team_size,
                                          max_clock_tick,
                                          number_of_projects=25,
                                          number_of_traces=10,
                                          max_trace_length=750,
                                          random=random)

    projects_group.build_and_operate()


    def entry_point_name_is(task_func):
        return lambda t: t.entry_point_func.func_name == task_func.im_func.func_name

    def parent_entry_point_name_is(task_func):
        return lambda t: t.parent is not None and entry_point_name_is(task_func)(t.parent)

    def entry_point_name_and_parent_name_are(task_func, parent_task_func):
        return lambda t: entry_point_name_is(task_func)(t) and parent_entry_point_name_is(parent_task_func)(t)

    results_format = (

        # Task counts
        ("#exec_wf", "%10d", projects_group.task_count(entry_point_name_is(Waterfall.allocate_tasks))),
        ("#exec_tdd", "%10d", projects_group.task_count(entry_point_name_is(TestDrivenDevelopment.implement_feature_tdd))),
        ("#exec_co", "%10d", projects_group.task_count(entry_point_name_is(ChangeManagement.commit_changes))),
        ("#exec_spc", "%10d", projects_group.task_count(entry_point_name_is(Specification.add_feature))),
        ("#exec_imp", "%10d", projects_group.task_count(entry_point_name_is(Implementation.implement_feature))),
        ("#exec_tng", "%10d", projects_group.task_count(entry_point_name_is(Testing.test_per_chunk_ratio))),
        ("#exec_dbg", "%10d", projects_group.task_count(entry_point_name_is(Debugging.debug_feature))),
        ("#exec_rfg", "%10d", projects_group.task_count(entry_point_name_is(Refactoring.refactor_feature))),

        # Fuzz counts
        ("#fuzz_wf", "%10d", fuzzi_moss.lines_removed_count(Waterfall)),
        ("#fuzz_tdd", "%10d", fuzzi_moss.lines_removed_count(TestDrivenDevelopment)),
        ("#fuzz_co", "%10d", fuzzi_moss.lines_removed_count(ChangeManagement)),
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
        ("#lines_imp", "%10d", fuzzi_moss.removable_lines_count(Implementation.implement_feature)),
        ("#lines_tng", "%10d", fuzzi_moss.removable_lines_count(Testing.test_per_chunk_ratio)),
        ("#lines_dbg", "%10d", fuzzi_moss.removable_lines_count(Debugging.debug_feature)),
        ("#lines_rfg", "%10d", fuzzi_moss.removable_lines_count(Refactoring.refactor_feature)),

        # Project characteristics
        ("mtf_avg", "%10.2f", projects_group.average_project_mean_time_to_failure),
        ("mtf", "%10s", projects_group.mean_times_to_failure),
        ("t_used", "%10d", projects_group.average_project_time_used),
        ("#ftrs_impld", "%10.2f", projects_group.average_project_features_implemented),
        ("#t_run", "%10d", projects_group.simulation_duration)
    )

    if not headers_printed:
        headers_printed = True
        results_file.write(format_headers(configuration_format + results_format) + '\n')

    results_file.write(format_row(configuration_format + results_format) + '\n')
    results_file.flush()

    pydysofu.reset_invocation_counters()
    fuzzi_moss.reset_lines_removed_counters()
    pydysofu.defuzz_all_classes()
