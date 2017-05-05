import matplotlib.pyplot as plt

from experiments.compare_workflows.data_for_plotting import get_time_series

plt.figure(figsize=(2.5, 2.5/1.4))

plt.rc('font', **{'family':'serif', 'serif':['Georgia'], 'size': 10})

plt.xlabel('#commits')
plt.ylabel('mtf_avg')

plt.xlim([0, 8000])
plt.ylim([0, 400])
plt.yticks([0, 100, 200, 300, 400])
plt.xticks([0, 4000, 8000])

x_values, y_values = get_time_series(
    x_field=lambda r: r.commits,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'WaterfallD' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, color='blue')

x_values, y_values = get_time_series(
    x_field=lambda r: r.commits,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'TestDriven' and r.fuzz_total <=0)

plt.scatter(x_values, y_values, color='red')

plt.savefig('mtf_against_commits_for_0_fuzz_simluations.jpg', bbox_inches='tight')