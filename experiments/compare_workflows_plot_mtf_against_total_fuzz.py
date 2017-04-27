import matplotlib.pyplot as plt
import numpy

from compare_workflows_data_for_plotting import get_time_series

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

plt.title('Average MTF against Total Fuzzings')
plt.xlabel('\#fuzzings')
plt.ylabel('\#mtf')

plt.xlim([0, 600])
plt.ylim([0, 300])

x_values, y_values = get_time_series(
    x_field=lambda r: r.fuzz_total,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'TestDriven')

plt.scatter(x_values, y_values, label='TDD', color='blue')

trend = numpy.poly1d(numpy.polyfit(x_values, y_values, 3))

plt.plot(x_values, trend(x_values),"b-")

x_values, y_values = get_time_series(
    x_field=lambda r: r.fuzz_total,
    y_field=lambda r: r.mtf_avg,
    row_filter=lambda r: r.workflow == 'WaterfallD')

plt.scatter(x_values, y_values, label='WTF', color='red')

p = numpy.poly1d(numpy.polyfit(x_values, y_values, 3))
plt.plot(x_values, p(x_values),"r-")

plt.legend(loc=0)

plt.show()
