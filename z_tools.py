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
    birth_decade_interest = range(1940, 2010 + 1, 10),
    bar_time_window = range(1980, 2060)
    )

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


def execute_or_load_cache(function):
    file_name = 'io/' + function.__qualname__ + '.pkl'
    if os.path.exists(file_name):
        outputs = pickle.load(open(file_name, 'rb'))
    else:
        outputs = function()
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
