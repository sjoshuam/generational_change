"""
    TODO: module description
"""

##########==========##########==========##########==========##########==========
## INITIALIZE ENVIRONMENT

## libraries
import numpy as np
import pandas as pd
import plotly.graph_objects as go


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
## IMPORT DATA
#### --> EXECUTE IMMEDIATELY SO DATASET CAN BE USED AS AN ARGUMENT DEFAULT

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

## execute import early 
life_expect = import_data()

##########==========##########==========##########==========##########==========
## DEFINE FUNCTIONS


def autofill_params(params = params):
    """
        Automatically fills in some useful parameters
    """
    ## determine the birth years to be displayed in the life chance tables
    params['current_yr'] = pd.Timestamp.now().year    
    params['birth_years'] = list(
        range(params['current_yr'] - 80, params['current_yr'] + 1, 20))


def calculate_survival_pct(birth_yr, le = life_expect, params = params):
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
    return le


def calculate_survival_for_all(params = params):
    """
        Iterate calculate_survival() for all birth years in params
    """
    survival_pct = list()
    for iter_birth in params['birth_years']:
        survival_pct.append(calculate_survival_pct(iter_birth))
    survival_pct = pd.concat(survival_pct, axis = 0).reset_index(drop = True)
    return survival_pct


##########==========##########==========##########==========##########==========
## EXECUTE FUNCTIONS

if __name__ == '__main__':

    ## automatically fill in some parameters
    autofill_params()

    ## calculate survival chances
    survival_pct = calculate_survival_for_all()

    ## save results
    survival_pct.to_excel('io/survival_pct.xlsx', index = False)


##########==========##########==========##########==========##########==========
