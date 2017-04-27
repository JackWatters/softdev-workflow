import matplotlib.pyplot as plt

from simulation_run_data_for_plotting import get_time_series

plt.title('Total Commits Against Total Chunks \nfor Small and Large Projects')
plt.xlabel('\#chunks')
plt.ylabel('\#commits')

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

plt.xlim([0, 25])
plt.ylim([0, 8000])

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

plt.legend(loc=4)

plt.show()
