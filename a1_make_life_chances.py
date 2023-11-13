"""
    Defines make_life_chances(), which calculates life expectancy statistics from CDC life tables
"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## import statements
import multiprocessing
import pandas as pd

## define parameters
params = {
    'current_year': pd.Timestamp.now().year,
    'birth_years': [pd.Timestamp.now().year - i for i in range(90, -1, -1)],
    'data': {'M':'in/a1_Table02_Male.xlsx', 'F':'in/a1_Table03_Female.xlsx'},
    'cpu_count': min(max(int(multiprocessing.cpu_count() *0.8), multiprocessing.cpu_count() -1), 8)
}

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def import_life_chances(params = params):
    """
        Function reads, compiles and reshapes life table data into a simple
        three column dataset.
    """
    life_chances = dict()
    for i in params['data'].keys():
        life_chances[i] = pd.read_excel(
            io = params['data'][i], skiprows = 2,index_col = 0, usecols = [0, 1])
    life_chances = pd.concat(life_chances, axis = 1).dropna().reset_index()
    life_chances.columns = life_chances.columns.droplevel(1)
    life_chances = life_chances.rename(columns = {'index': 'Age'})
    life_chances['Age'] = life_chances['Age'].str.replace('[– ].*','', regex=True)
    life_chances = life_chances.astype({'Age':int})
    return life_chances


def refine_life_chances(birth_year, life_chances, params = params):
    """
        Calculate the survival percentages from the present year for a given
        birth year
    """
    year_now = params['current_year']
    age_now = year_now - birth_year
    life_chances = life_chances.loc[life_chances['Age'] >= age_now].copy()
    life_chances['Yr'] = life_chances['Age'] - min(life_chances['Age']) + year_now
    life_chances['M'] = (1 - life_chances['M']).cumprod()
    life_chances['F'] = (1 - life_chances['F']).cumprod()
    life_chances['Birthyear'] = birth_year
    life_chances = pd.melt(
        frame = life_chances.drop(columns = 'Yr'),
        id_vars = ['Birthyear', 'Age'],
        value_vars = ['M', 'F'],
        var_name = 'Sex',
        value_name = 'Alive'
    )
    return life_chances.set_index(['Sex', 'Birthyear'])


##########==========##########==========##########==========##########==========##########==========
## PARALLEL PROCESSING CONVENIENCE FUNCTION


def refine_life_chances_iterator(birth_years, life_chances, params = params):
    """
        Iterarates refine_life_chances() over a list of input values; enabling parallel processing
    """
    return [refine_life_chances(byrs, life_chances = life_chances) for byrs in birth_years]


def split_up_birth_years(params = params):
    """
        Splits a list of integers into chunks; enabling parallel processing
    """
    splits = [list() for i in range(0, params['cpu_count'])]
    [splits[i % params['cpu_count']].append(i) for i in params['birth_years']]
    return splits
    

##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION


def make_life_chances(params = params):
    """
        Executes refine_life_chances() in  
    """

    ## import life chance data
    life_chances = import_life_chances()

    ## refine life chance data in parallel
    pool, parallel_output = multiprocessing.Pool(params['cpu_count']), list()
    for iter_birthyears in split_up_birth_years():
        parallel_output.append(
            pool.apply_async(
                func = refine_life_chances_iterator, 
                kwds = {'birth_years': iter_birthyears, 'life_chances': life_chances}
                )
            )
    parallel_output = [pd.concat(i.get(), axis = 0) for i in parallel_output]
    pool.close()
    life_chances = pd.concat(parallel_output, axis = 0).sort_index().round({'Alive':3})
    life_chances.to_excel('io/a1_life_chances.xlsx')
    return life_chances


##########==========##########==========##########==========##########==========##########==========
## TEST CODE


if __name__ == '__main__':
    life_chances = make_life_chances()


##########==========##########==========##########==========##########==========##########==========
