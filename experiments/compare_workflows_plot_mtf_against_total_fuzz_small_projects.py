import matplotlib.pyplot as plt
import numpy

from compare_workflows_data_for_plotting import get_time_series, project_sizes

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

plt.title('Average MTF against Total Fuzzings for Small Feature Projects')
plt.xlabel('\#fuzzings')
plt.ylabel('\#mtf')

plt.xlim([0, 600])
plt.ylim([0, 250])

for workflow in ['TestDriven', 'WaterfallD']:

    for project_size in sorted(project_sizes('small').values())[1:]:

        x_values, y_values = get_time_series(
            x_field=lambda r: r.fuzz_total,
            y_field=lambda r: r.mtf_avg,
            row_filter=lambda r:
                r.workflow == workflow and r.project_size == project_size and r.project_type == 'small')

        d = 1 - project_size/ (1.0 * max(project_sizes('small').values()))

        color = (1.0, d, d) if workflow is 'WaterfallD' else (d, d, 1.0)

        plt.scatter(x_values, y_values, label=workflow+" "+str(project_size), color=color)

        trend = numpy.poly1d(numpy.polyfit(x_values, y_values, 2))

        plt.plot(x_values, trend(x_values),color=color)

plt.legend(loc=0)

plt.show()
