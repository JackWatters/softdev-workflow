import matplotlib.pyplot as plt
import numpy

from experiments.compare_workflows.data_for_plotting import get_time_series, project_sizes


for fuzz_type in ['WT', 'CTIDR']:

    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 8})
    plt.rc('text', usetex=True)
    plt.figure(figsize=(2, 2 / 1.4))

    plt.xlabel('\#statements removed')
    plt.ylabel('\#features completed')

    plt.xlim([0, 600])
    plt.ylim([0, 7])

    for project_type in ['small', 'large']:
        for workflow in ['TestDriven', 'WaterfallD']:

            for project_size in sorted(project_sizes(project_type).values()):

                x_values, y_values = get_time_series(
                    x_field=lambda r: r.fuzz_total,
                    y_field=lambda r: r.features_implemented,
                    row_filter=lambda r:
                        r.workflow == workflow and r.project_size == project_size and r.project_type == project_type and r.fuzz_type == fuzz_type)

                d = 1 - project_size/ (1.0 * max(project_sizes(project_type).values()))

                color = (1.0, d, d) if workflow is 'TestDriven' else (d, d, 1.0)
                label = workflow+" "+project_type+" "+str(project_size)

                plt.scatter(x_values, y_values, label=label, color=color)

                trend = numpy.poly1d(numpy.polyfit(x_values, y_values, 2))

                plt.plot(x_values, trend(x_values), color=color)

    plt.tight_layout(pad=0)
    plt.savefig('features_against_total_fuzz_%s.pdf' % fuzz_type)
    plt.close()