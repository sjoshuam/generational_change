"""
    Declares sets of generic functions for doing common operations:
        Parallelization - index-based map/reduce parallelization
        Caching - Saving outputs for use in downstream scripts during testing
"""
##########==========##########==========##########==========##########==========##########==========
## HEADER

import multiprocessing, pickle, os

params = dict(
    n_cores = min(max(multiprocessing.cpu_count() - 1, 1), 4),
    dark = '#663D14', light = '#FFF9F2',
    birth_decade_interest = range(1940, 2020, 10),
    bar_time_window  = range(1980, 2060),
    proj_time_window = range(2020, 2080),
    migrant_rate = [1.05, 1.10, 1.15, 1.20, 1.25, 1.30],
    cohort_pct = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    margin = 2**3
    )

params['cohort_colors'] = {
    'Other':  params['light'],
    1940:    'hsv(345, 0.5, 0.50)',
    1950:    'hsv(355, 0.5, 0.60)',
    1960:    'hsv(005, 0.5, 0.70)',
    1970:    'hsv(015, 0.5, 0.80)',
    1980:    'hsv(165, 0.5, 0.50)',
    1990:    'hsv(175, 0.5, 0.60)',
    2000:    'hsv(185, 0.5, 0.70)',
    2010:    'hsv(195, 0.5, 0.80)',
}

params['lean_colors'] = {
    'con':  'hsv( 15, 0.5, 0.9)',
    'lib':  'hsv(195, 0.5, 0.7)',
    'either': params['dark'],
    'none': params['light'],
}

##########==========##########==========##########==========##########==========##########==========
## UTILITY FUNCTIONS - PARALLELIZATION


def split_index(index = list[int], n_cores = params['n_cores']) -> list[list]:
    """
        Purpose: Subsets a list of indices into separate lists that can be supplied to a function
            for processsing in parallel.
        Arguments: TODO
        Return: A list of lists, each of which can be supplied to parallel executions of a function
    """
    split_index = [[] for i in range(0, n_cores)]
    for iter_index in index:
        split_index[iter_index % n_cores] = split_index[iter_index % n_cores] + [iter_index]
    return split_index


def execute_in_parallel(map_function, reduce_function,
        indices: list[list], n_cores = params['n_cores'], **kwargs: dict):
    """
        Purpose: executes a function in parallel chunks and then aggregates the chunks together
        Arguments:
            map_function: function executed in parallel
            reduce_function: function used to aggregate outputs from map_function
            indices: A list of lists indicates the chunks of a problem that should be fed to each
                map_function instance for parallel processing.
    """
    pool = multiprocessing.Pool(min(len(indices), 8))
    parallel_output = list()
    for iter_index in indices:
        kwargs.update({'index':iter_index})
        parallel_output.append(pool.apply_async(func = map_function, kwds = kwargs.copy()))
    parallel_output = [x.get() for x in parallel_output]
    pool.close()
    return reduce_function(parallel_output)


def reduce_freq_counts(x: list[dict]) -> dict:
    """Sums a list of frequency count dict into a single dict"""
    for iter_list in range(1, len(x)):
        for iter_key in x[iter_list].keys():
            x[0][iter_key] = x[0].get(iter_key, 0) + x[iter_list][iter_key]
    return x[0]


def map_freq_counts(value_list: list, index: list) -> dict:
    """Counts values in a list, formulated for parallel execution"""
    value_count = dict()
    for iter_index in index:
        value_count[value_list[iter_index]] = value_count.get(value_list[iter_index], 0) + 1
    return value_count


##########==========##########==========##########==========##########==========##########==========
## UTILITY FUNCTIONS - CACHING


def execute_or_load_cache(function, **kwargs):
    file_name = 'io/' + function.__qualname__ + '.pkl'
    if os.path.exists(file_name):
        print('execute_or_load_cache(): Loading From Cache')
        outputs = pickle.load(open(file_name, 'rb'))
    else:
        outputs = function(**kwargs)
        pickle.dump(outputs, open(file_name, 'wb'))
    return outputs



##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':

    ## test parallelization tools
    parallel_in = ['a' for i in range(0, 20)] + ['b' for i in range(0, 30)]
    parallel_out = execute_in_parallel(
        map_function = map_freq_counts,
        reduce_function = reduce_freq_counts,
        indices= split_index(list(range(0, len(parallel_in)))),
        value_list = parallel_in
        )

##########==========##########==========##########==========##########==========##########==========
