"""
    TODO: module description
"""

##########==========##########==========##########==========##########==========
## INITIALIZE ENVIRONMENT

## libraries
import pandas as pd

## parameters
"""
    MANUAL PARAMETERS
    'data': relative location of life table files, ready for read-in

    AUTOMATICALLY GENERATED PARAMETERS
    'current_year': the current year
    'birth_years': five birth years to be displayed in life chance charts
"""

params = {
    'data': {'M':'in/Table02_Male.xlsx', 'F':'in/Table03_Female.xlsx'}
}

##########==========##########==========##########==========##########==========
## DEFINE FUNCTIONS


def autofill_params(params = params):
    """
        Automatically fills in some useful parameters, like the
        current year and years to be used for displaying life
        chances.
    """
    params['current_yr'] = pd.Timestamp.now().year    
    params['birth_years'] = list(
        range(params['current_yr'] - 90, params['current_yr'] + 1, 1))


def import_data(params = params):
    """
        Function reads, compiles and reshapes life table data into a simple
        three column dataset.
    """
    life_expect = dict()
    for i in params['data'].keys():
        life_expect[i] = pd.read_excel(
            io = params['data'][i], skiprows = 2,
            index_col = 0, usecols = [0, 1]
        )
    life_expect = pd.concat(life_expect, axis = 1).dropna().reset_index()
    life_expect.columns = life_expect.columns.droplevel(1)
    life_expect = life_expect.rename(columns = {'index': 'Age'})
    life_expect['Age'] = life_expect['Age'].str.replace('[– ].*','', regex=True)
    life_expect = life_expect.astype({'Age':int})
    return life_expect


def calculate_survival_pct(birth_yr, le, params = params):
    """
        Calculate the survival percentages from the present year for a given
        birth year
    """
    current_age = params['current_yr'] - birth_yr
    le = le.loc[le['Age'] >= current_age].copy()
    le['Yr'] = le['Age'] - min(le['Age']) + params['current_yr']
    le['M'] = (1 - le['M']).cumprod()
    le['F'] = (1 - le['F']).cumprod()
    le['Birthyear'] = birth_yr
    le = pd.melt(
        frame = le.drop(columns = 'Yr'),
        id_vars = ['Birthyear', 'Age'],
        value_vars = ['M', 'F'],
        var_name = 'Sex',
        value_name = 'Alive'
    ).set_index(['Sex', 'Birthyear'])
    return le


def calculate_survival_for_all(le, params = params):
    """
        Iterate calculate_survival() for all birth years in params
    """
    survival_pct = list()
    for iter_birth in params['birth_years']:
        survival_pct.append(calculate_survival_pct(iter_birth, le))
    survival_pct = pd.concat(survival_pct, axis = 0)
    return survival_pct


##########==========##########==========##########==========##########==========
## EXECUTE FUNCTIONS

if __name__ == '__main__':

    ## automatically fill in some parameters
    autofill_params()

    ## import data
    life_expect = import_data()

    ## calculate survival chances
    survival_pct = calculate_survival_for_all(life_expect)

    ## save results
    survival_pct.to_excel('io/survival_pct.xlsx')

##########==========##########==========##########==========##########==========
