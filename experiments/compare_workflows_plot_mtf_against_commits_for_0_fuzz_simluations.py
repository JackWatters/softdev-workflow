import matplotlib.pyplot as plt

from compare_workflows_data_for_plotting import get_time_series

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

plt.title('Average Mean Time to Failure Against Commits')
plt.xlabel('\#commits')
plt.ylabel('mtf_avg')

plt.xlim([0, 8000])
plt.ylim([0, 350])

x_values, y_values = get_time_series(
    x_field=lambda r: r.commits,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'TestDriven' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, label='TDD')

x_values, y_values = get_time_series(
    x_field=lambda r: r.commits,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'WaterfallD' and r.fuzz_total <=0)

plt.scatter(x_values, y_values, label='WTF', color='red')

plt.legend(loc=0)

plt.show()
