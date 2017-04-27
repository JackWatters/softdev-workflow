import csv

small_project_size = {
    '0': 2,
    '0 1': 4,
    '0 1 2' : 6,
    '0 1 2 3': 8,
    '0 1 2 3 4': 10,
    '0 1 2 3 4 5': 12,
}

large_project_size = {
    '6': 4,
    '6 7': 8,
    '6 7 8' : 12,
    '6 7 8 9': 16,
    '6 7 8 9 10': 20,
    '6 7 8 9 10 11': 24,
}

all_project_sizes = small_project_size.copy()
all_project_sizes.update(large_project_size)


class SimulationRun(object):

    def __init__(self, raw):
        self.raw = raw

    @property
    def project_spec(self):
        return self.raw[' #ftrs_spec'].strip()

    @property
    def project_type(self):
        if self.project_spec in small_project_size.keys():
            return 'small'
        elif self.project_spec in large_project_size.keys():
            return 'large'

    @property
    def commits(self):
        return self.raw['   #exec_co']

    @property
    def project_size(self):
        return all_project_sizes[self.project_spec]

    @property
    def mtf_avg(self):
        return float(self.raw['    mtf_avg'])

    @property
    def fuzz_total(self):
        return int(self.raw['  #fuzz_tot'])

    @property
    def workflow(self):
        return self.raw['  workflow']

    @property
    def t_used(self):
        return int(self.raw['     t_used'])


simulation_runs = [SimulationRun(row) for row in csv.DictReader(open('compare_workflows.csv','r'))]


def get_time_series(x_field, y_field, row_filter=lambda r: True):
    series = sorted([(x_field(row), y_field(row)) for row in simulation_runs if row_filter(row)])
    return map(lambda t: t[0], series), map(lambda t: t[1], series)

