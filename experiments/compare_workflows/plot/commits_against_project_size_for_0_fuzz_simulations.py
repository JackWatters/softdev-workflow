import matplotlib.pyplot as plt

from experiments.compare_workflows.data_for_plotting import get_time_series

plt.rc('font', **{'family':'serif', 'serif':['Georgia'], 'size': 10})

plt.figure(figsize=(2.5, 2.5/1.4))

plt.xlabel('#chunks')
plt.ylabel('#commits')

plt.xlim([0, 25])
plt.ylim([0, 8000])
plt.yticks([0, 2000, 4000, 6000, 8000])

x_values, y_values = get_time_series(
    x_field=lambda r: r.project_size,
    y_field=lambda r: r.commits,
    row_filter=lambda r: r.project_type == 'small' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, label='Small Feature Projects', color='blue')

x_values, y_values = get_time_series(
    x_field=lambda r: r.project_size,
    y_field=lambda r: r.commits,
    row_filter=lambda r: r.project_type == 'large' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, label='Large Feature Projects', color='red')

plt.savefig('commits_against_project_size_for_0_fuzz_simulations.jpg', bbox_inches='tight')
