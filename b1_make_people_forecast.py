##########==========##########==========##########==========##########==========##########==========
## INITIALIZE

## import libraries
import multiprocessing
import pandas as pd


##########==========##########==========##########==========##########==========##########==========
## GENERIC UTILITY FUNCTIONS


def split_index(index = list[int], n_cores = 4) -> list[list]:
    split_index = [[] for i in range(0, n_cores)]
    for iter_index in index:
        split_index[iter_index % n_cores] = split_index[iter_index % n_cores] + [iter_index]
    return split_index


def execute_in_parallel(map_function, reduce_function, indices: list[list], **kwargs: dict):
    """
        Purpose: executes a function in parallel chunks and then aggregates the chunks together
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
    return reduce_function(parallel_output)


##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS - BIRTH

def import_birth(year_range = [1930, 2100]) -> pd.DataFrame:
    """
        Purpose: imports data files for this panel
            historic_birth: TODO
            future_birth: TODO
            historic_people: TODO
        Arguments:
            year_range: defines the range of years for which data will be compiled
        Outputs: A composite dataframe of all data needed to render this panel
    """

    ## read in files
    historic_birth = pd.read_excel('in/b1_historic_births.xlsx', sheet_name = 'data')
    future_birth = pd.read_excel('in/b1_future_population.xlsx', sheet_name = 'np2023_d1_zero',
        usecols = ['SEX', 'ORIGIN', 'YEAR', 'RACE', 'POP_0', 'TOTAL_POP'])
    future_birth = future_birth.rename(columns = {'YEAR': 'year', 'TOTAL_POP':'people'})
    historic_people = pd.read_excel('in/b1_historic_population.xlsx',
        sheet_name = 'data', usecols = ['year', 'people'])
    
    ## reshape future births
    future_birth['SEX'] = future_birth['SEX'].replace({0:'birth_all', 1:'male', 2:'fem'})
    future_birth = future_birth.loc[(future_birth['ORIGIN'] + future_birth['RACE']) == 0]
    future_birth = future_birth.drop(columns = ['ORIGIN', 'RACE']).pivot_table(index = 'year',
        columns = 'SEX', values = ['POP_0', 'people'], aggfunc = sum).reset_index()
    future_birth.columns.name = None
    future_birth = pd.concat(
        [future_birth[['year']], future_birth[('POP_0')], future_birth[('people', 'birth_all')]],
        axis = 1).rename(columns = {('year', ''): 'year', ('people', 'birth_all'): 'people'})
    future_birth['male_pct'] = future_birth['male'] / future_birth['birth_all']
    
    ## fuse datasets and standardized
    birth = pd.concat([historic_birth, future_birth], axis = 0).sort_values('year')
    index = pd.DataFrame({'year': list(range(min(year_range), max(year_range)+ 1))})
    birth = index.merge(birth, how = 'left', on = 'year').copy()
    birth = birth.merge(historic_people.rename(columns= {'people': 'x'}), how= 'left', on= 'year')
    birth.loc[birth['people'].isna(), 'people'] = birth.loc[birth['people'].isna(), 'x']
    birth = birth.drop(columns = 'x')

    return birth


def interpolate_missing_birth(birth: pd.DataFrame) -> pd.DataFrame:
    """
        TODO: FILL THIS IN
    """
    ## fill in missing intermediate values by linear interpolation
    birth = birth.interpolate(limit_direction = 'both', limit_area = 'inside')
    birth['male_pct'] = birth['male_pct'].fillna(birth['male_pct'].mean())

    ## infer birthrate from earliest value
    birth['birth_rate'] = (birth['birth_all'] / birth['people'])
    birth['birth_rate'] = birth['birth_rate'].fillna(birth['birth_rate'].dropna().iloc[0])

    ## deduce births from people * birth_rate
    idx = birth['birth_all'].isna()
    birth.loc[idx, 'birth_all'] = birth.loc[idx, 'people'] * birth.loc[idx, 'birth_rate']

    ## deduce male/female births
    idx = birth['male'].isna()
    birth.loc[idx, 'male'] = birth.loc[idx, 'male_pct'] * birth.loc[idx, 'birth_all']
    birth.loc[idx, 'fem'] = birth.loc[idx, 'birth_all']  - birth.loc[idx, 'male']

    ## clean up number types and precision
    birth = birth.astype({i:int for i in ['male', 'fem', 'birth_all', 'people']})
    people = birth[['year', 'people']].copy().set_index('year')
    birth = birth[['year', 'male', 'fem']].set_index('year')

    return birth, people


##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS - DEATH AND MIGRATION


def map_death(index: list[list, str]) -> pd.DataFrame:
    """
        Purpose: Imports mortality chance data.  Function designed for parallelization for the sake
            of practicing useful skills.
        Arguments: a list of problem chunks that can be done in parallel
        Returns: a data frame of mortality chances at each age for a given gender
    """
    death = pd.read_excel('in/' + index, skiprows = 2).rename(columns = {'Unnamed: 0': 'age'})
    death = death[['age', 'qx']].dropna().set_index('age').drop('100 and over')
    death.index = death.index.str.replace('[–].+', '', regex = True).astype(int)
    if index.find('Female') > -1: death.columns = ['fem']
    else: death.columns = ['male']

    return death


def reduce_death(death: pd.DataFrame) -> pd.DataFrame:
    """Aggregates parallelized outputs from map_death()"""
    return pd.concat(death, axis = 1)


def simulate_migrant(death: pd.DataFrame, rate: float) -> pd.DataFrame:
    """
        Purpose: For a given overall migration rate, simulate per year, per gender net migration
            rates.  In the absense of better data, this is used to increase birth cohorts over
            time to reflect net migration chances to the size of each birth year cohort.
        Arguments:
            death: A dataset of per year per gender chances of death
            rate: An overall migration rate
        Return: Per year, per gender migration rate dataframe
    """
    rate = {'male': 1 + ((rate-1) * 0.6), 'fem': 1 + ((rate-1) * 0.4)}
    per_year = dict(1 / ((1 - death).sum()))
    migrant = ((death * 0) + 1).copy()
    migrant['male'] *= rate['male']**per_year['male']
    migrant['fem'] *= rate['fem' ]**per_year['fem']
    return migrant


##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS - COHORT SIZE


def project_cohort_size_over_time(birth_year:int, birth: pd.DataFrame,
        migrant: pd.DataFrame, death: pd.DataFrame)-> pd.DataFrame:
    """
        Purpose: Projects the population size of a US birth year cohort over time, based on
            migration (increases cohort population over time) and death rates (decreases pop.)
        Arguments:
            birth_year:
            birth: TODO
            migrant: TODO
            death: TODO
        Return: a year x gender dataframe ennumerating the size of birth cohorts in a given year
    """
    cohort_size = ((1 - death).cumprod() * migrant.cumprod() * birth.loc[birth_year]).reset_index()
    cohort_size['year'] = (cohort_size['age'] + birth_year)
    cohort_size = cohort_size.round().astype(int)
    return cohort_size


def reduce_cohort_size_over_time(cohort_size: list) -> pd.DataFrame:
    """TODO"""
    return pd.concat(cohort_size, axis = 0)


def map_cohort_size_over_time(index: list[list], birth: pd.DataFrame, migrant: pd.DataFrame,
        death: pd.DataFrame, reduce_function = reduce_cohort_size_over_time):
    """
        TODO
    """
    cohort_size = list()
    for iter_index in index:
        cohort_size.append(project_cohort_size_over_time(
            birth_year = iter_index, birth = birth, migrant = migrant, death = death))
    cohort_size = reduce_function(cohort_size)
    return cohort_size


def aggregate_cohorts_to_birth_decades(cohort_size):
    """
        TODO
    """
    cohort_size = cohort_size.copy()
    cohort_size['birth_decade'] = ((cohort_size['year'] - cohort_size['age']) // 10) * 10
    birth_decade_forecast = cohort_size.groupby(['birth_decade', 'year']).sum().drop(columns= 'age')
    return birth_decade_forecast


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION


def make(migrant_rate = 1.03):
    """
        TODO
    """

    ## get sizes of birth cohorts
    birth = import_birth()
    birth, people = interpolate_missing_birth(birth)

    ## get mortality chances per age per gender
    death = execute_in_parallel(
        map_function = map_death, reduce_function = reduce_death,
        indices = ['a1_Table02_Male.xlsx', 'a1_Table03_Female.xlsx'])
    
    ## simulate migration chances per age per gender
    migrant = simulate_migrant(death = death, rate = migrant_rate)

    ## project cohort size at each age and calendar year
    cohort_size = execute_in_parallel(
        map_function = map_cohort_size_over_time,
        reduce_function = reduce_cohort_size_over_time,
        indices = split_index(list(range(1930, 2030))),
        birth = birth, migrant = migrant, death = death
        )

    ## aggregate cohort size to birth decades
    birth_decade_forecast = aggregate_cohorts_to_birth_decades(cohort_size)

    ## export
    cohort_size.to_excel('io/b1_people_forecast.xlsx', index = False)
    birth_decade_forecast.to_excel('io/b1_birth_decade_forecase.xlsx')
    return cohort_size, birth_decade_forecast


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    cohort_size, birth_decade_forecast = make()
    
    
    

##########==========##########==========##########==========##########==========##########==========
