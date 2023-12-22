"""
    TODO
"""

##########==========##########==========##########==========##########==========##########==========
## HEADER

import pandas as pd
import z_tools, b1_make_people_forecast
import numpy as np

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def import_weight_data():
    """Import raw datasets"""
    url = 'in/c0_weight_data.xlsx'
    wealth = pd.read_excel(url, sheet_name = 'wealth', header = 0)
    vote   = pd.read_excel(url, sheet_name = 'vote', header = 0, index_col = 0)
    return wealth, vote


def refine_vote_data(vote):
    """
        TODO:
    """

    ## reshape data to con/lib/mod/none percentages for each year of date
    vote = vote.melt(var_name = 'vote', value_name = 'count', ignore_index = False).reset_index()
    vote['vote'] = vote['vote'].str.slice(0, 1).astype(int).replace({
        1:1, 2:1, 3:1, 4:2, 5:3, 6:3, 7:3, 9:4}).replace({1:"lib", 2:'mod', 3:'con', 4:'none'})
    vote = vote.rename(columns = {'index': 'age'}).groupby(['age', 'vote']).sum().reset_index()
    vote = pd.pivot(vote, columns = 'vote', index = 'age', values = 'count')
    vote = vote.div(vote.sum(axis = 1), axis = 0)
    vote = vote.rolling(window = 5, center = True, min_periods = 1).mean()

    ## reallocate moderates to other categories
    mods = vote[['con', 'lib', 'none']].div(vote[['con', 'lib', 'none']].sum(axis = 1), axis = 0)
    mods = mods.mul(vote['mod'], axis = 0)
    vote = vote[['con', 'none', 'lib']] + mods[['con', 'none', 'lib']]
    del mods

    ## infer children and elderly
    idx = pd.DataFrame({'age':range(0, 100)})
    vote = idx.merge(vote, how = 'left', on = 'age')
    vote.loc[vote['age'] < 18, ['con', 'lib']] = 0
    vote.loc[vote['age'] < 18, ['none']] = 1
    vote = vote.interpolate(axis = 'index', limit_direction = 'both')

    ## return results
    return vote.round(6)


def refine_wealth_data(wealth):
    """
        TODO:
    """

    ## extract data and reshape
    wealth = wealth.set_index(['wealth_min', 'wealth_max'])
    wealth = wealth.rolling(window = 5, center = True, axis = 1, min_periods = 1).sum()
    inequality = pd.Series(wealth.sum(axis = 1).reset_index(drop = True), name = 'weight')
    inequality /= inequality.sum() / 1000
    wealth = (wealth / wealth.sum()).reset_index()
    inequality = pd.concat([wealth[['wealth_min', 'wealth_max']], inequality], axis= 1).astype(int)
    wealth = wealth.drop(columns = ['wealth_min', 'wealth_max'])

    ## interpolate missing data
    kids = pd.DataFrame(np.zeros((wealth.shape[0], 18)))
    kids.loc[0] = 1
    wealth = pd.concat([kids, wealth], axis = 1)
    for iter in range(max(wealth.columns) + 1, 100):
        wealth[iter] =  wealth[max(wealth.columns)].copy()
    wealth = wealth.transpose().reset_index().rename(columns = {'index': 'age'})

    return wealth.round(6), inequality


def gini(x):
    """Calculate Gini Coefficient"""
    return (np.abs(np.subtract.outer(x, x)).mean() / np.mean(x)) * 0.5


def make_inequality_scenarios(inequality, approach = 'modeled'):
    """
        TODO
    """
    n = 7

    ## generate scenarios (empircal)
    if approach == 'empirical':
        scenarios = np.ones((inequality.shape[0], n)) * np.linspace(0, 1, n)
        scenarios = (
            inequality['wealth_min'].values.reshape(-1,1) * (1 - scenarios) + 
            inequality['wealth_max'].values.reshape(-1,1) * scenarios 
            )
    if approach == 'modeled':
        n = np.array([1.2, 1.29, 1.37, 1.52, 1.70, 2.00, 2.65])
        x = np.ones((inequality.shape[0], len(n))) * n
        for iter in range(0, x.shape[0]):
            x[iter, :] = x[iter, :]**iter
    else:
        raise Exception('Approach is not a valid option')
    scenarios = pd.DataFrame(x).astype(int)
    
    ## calculate gini coefficients for each scenario (for dev use only)
    scenario_gini = dict()
    for iter_scenario in scenarios.columns:
        gini_now = np.repeat(scenarios[iter_scenario].values, inequality['weight'].values)
        scenario_gini[iter_scenario] = gini(gini_now)
    scenario_gini = pd.Series(scenario_gini, name = 'scenario_gini').round(2)

    return scenarios, scenario_gini



##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS

##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    ## people_forecast = z_tools.execute_or_load_cache(b1_make_people_forecast.make_b1)[0]

    wealth, vote = import_weight_data()

    vote = refine_vote_data(vote)

    wealth, inequality = refine_wealth_data(wealth)
    scenarios, scenario_gini = make_inequality_scenarios(inequality)
    
    print(wealth)
    print(scenarios)
    print(scenario_gini)

##########==========##########==========##########==========##########==========##########==========
