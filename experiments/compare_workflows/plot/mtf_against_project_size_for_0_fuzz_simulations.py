import matplotlib.pyplot as plt

from experiments.compare_workflows.data_for_plotting import get_time_series

plt.rc('font', **{'family':'serif', 'serif':['Computer Modern'], 'size': 8})
plt.rc('text', usetex=True)

plt.figure(figsize=(2, 2.0/1.4))

plt.xlabel('\#chunks')
plt.ylabel('mtf\_avg')

plt.xlim([0, 25])
plt.ylim([0, 400])
plt.yticks([0, 100, 200, 300, 400])

x_values, y_values = get_time_series(
    x_field=lambda r: r.project_size,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'WaterfallD' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, color='blue')

x_values, y_values = get_time_series(
    x_field=lambda r: r.project_size,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'TestDriven' and r.fuzz_total <= 0)

plt.scatter(x_values, y_values, color='red')
plt.tight_layout(pad=0)
plt.savefig('mtf_against_project_size_for_0_fuzz_simulations.pdf')