import matplotlib.pyplot as plt
import numpy

from experiments.compare_workflows.data_for_plotting import get_time_series, project_sizes

for project_type in ['small', 'large']:

    plt.figure(figsize=(3, 3/1.4))

    plt.rc('font', **{'family': 'serif', 'serif': ['Georgia'], 'size': 10})

    plt.xlabel('#statements removed')
    plt.ylabel('#mtf')

    plt.xlim([0, 600])
    if project_type == 'small':
        plt.ylim([0, 250])
    else:
        plt.ylim([0,50])

    for workflow in ['TestDriven', 'WaterfallD']:

        for project_size in sorted(project_sizes(project_type).values())[1:]:

            x_values, y_values = get_time_series(
                x_field=lambda r: r.fuzz_total,
                y_field=lambda r: r.mtf_avg,
                row_filter=lambda r:
                    r.workflow == workflow and
                    r.project_size == project_size and
                    r.project_type == project_type)

            d = 1 - project_size/ (1.0 * max(project_sizes(project_type).values()))

            color = (1.0, d, d) if workflow is 'TestDriven' else (d, d, 1.0)

            plt.scatter(x_values, y_values, color=color)

            trend = numpy.poly1d(numpy.polyfit(x_values, y_values, 2))

            plt.plot(x_values, trend(x_values),color=color)

    plt.savefig('mtf_against_total_fuzz_large_projects_%s.jpg' % project_type, bbox_inches='tight')
    plt.close()

