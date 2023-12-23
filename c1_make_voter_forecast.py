"""
    Module projects US political leanings from population projections, differentiated by birth
    year and age.  Based on the American National Election Survey, we can roughly estimate how
    the political leaning of each age group in the American population.  However, these leanings
    can be attributed to age and/or cohort:

    - Age:  Older Americans tend to be more conservative because they are older.
    - Cohort: Older Americans tend to be more conservative because of the decades in which their
    formative live experiences happened.

    This module makes multiple projections, where each projection makes different assumptions
    about the relative power of age versus cohort in predicting future political leanings. The
    output is a pd.DataFrame of projections, ready for visualization.

"""

##########==========##########==========##########==========##########==========##########==========
## HEADER

import pandas as pd
import z_tools, b1_make_people_forecast
import numpy as np

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def simplify_people_forecast(pf: pd.DataFrame) -> pd.DataFrame:
    """Removes unneeded complexity from people forecast"""
    return pd.DataFrame({'people':pf.loc[1.15].sum(axis = 1)}).reset_index()


def import_vote_data():
    """Imports ANES data on political leanings by age"""
    url = 'in/c0_weight_data.xlsx'
    vote   = pd.read_excel(url, sheet_name = 'vote', header = 0, index_col = 0)
    return vote


def refine_vote_data(vote: pd.DataFrame, params = z_tools.params) -> pd.DataFrame:
    """
        shapes and refines ANES data on political leanings by age group
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


def project_pure_age_scenario(
        people_forecast: pd.DataFrame, vote: pd.DataFrame, params = z_tools.params) -> pd.DataFrame:
    """
        Projects political leanings based on the assumption that leaning is purely a function of
        age.
    """
    cause_age = people_forecast.merge(right = vote, how = 'left', on = 'age')
    for iter_politic in ['con', 'none', 'lib']:
        cause_age[iter_politic] = cause_age[iter_politic] * cause_age['people']
    cause_age = cause_age.drop(columns = 'people').round(6)
    cause_age = cause_age.loc[cause_age['year'].isin(params['proj_time_window'])]
    return cause_age.sort_values(['year', 'age'])


def project_pure_cohort_scenario(
        people_forecast: pd.DataFrame, vote: pd.DataFrame, params = z_tools.params) -> pd.DataFrame:
    """
        Projects political leanings based on the assumption that learning is purely a function of
        cohort.
    """
    ## assume children will vote like the 18 year old cohort
    cause_cohort = vote.copy()
    cause_cohort.loc[vote['age'] < 18, ['con', 'none', 'lib']] = np.nan
    cause_cohort = cause_cohort.interpolate(limit_direction = 'backward')

    ## make participation rate and partisanship percentages independent
    cause_cohort['lib'] = cause_cohort['lib'] / (cause_cohort['con'] + cause_cohort['lib'])
    cause_cohort['con'] = 1 - cause_cohort['lib']
    cause_cohort['cohort'] = min(params['proj_time_window']) - cause_cohort['age']

    ## incorporate lib/con percentages by cohort; participation by age
    people_forecast['cohort'] = people_forecast['year'] - people_forecast['age']
    people_forecast.loc[people_forecast['cohort'] > 2020, 'cohort'] = 2020
    cause_cohort = people_forecast.merge(
        right = cause_cohort[['con', 'lib', 'cohort']], how = 'left', on = 'cohort').merge(
            right = cause_cohort[['age', 'none']], how = 'left', on = 'age'
        )
    people_forecast = people_forecast.drop(columns = 'cohort')
    cause_cohort = cause_cohort.drop(columns = 'cohort')

    ## readjust totals so that lib + con + none = 1, reset children to 0% participation
    for iter_col in ['con', 'lib']: cause_cohort[iter_col] *= (1 - cause_cohort['none'])
    cause_cohort.loc[cause_cohort['age'] < 18, ['con', 'lib']] = 0
    cause_cohort.loc[cause_cohort['age'] < 18, ['none']] = 1

    ## convert percentages to headcounts and return
    for iter_politic in ['con', 'none', 'lib']:
        cause_cohort[iter_politic] = cause_cohort[iter_politic] * cause_cohort['people']
    cause_cohort = cause_cohort.loc[cause_cohort['year'].isin(params['proj_time_window'])]
    cause_cohort = cause_cohort.drop(columns = 'people').round(6)
    return cause_cohort.sort_values(['year', 'age'])


def project_age_cohort_mix(
        cause_age: pd.DataFrame, cause_cohort: pd.DataFrame, pct_cohort: float) -> pd.DataFrame:
    """
        Constructs a weighted average of political leanings projections based on age projections
        based on cohort.  This corresponds to making a specific assumption about the relative
        influence of age and cohort effects on political leanings.
    """
    cause_age = cause_age.set_index(['year', 'age']) * (1 - pct_cohort)
    cause_cohort = cause_cohort.set_index(['year', 'age']) * pct_cohort
    projection = (cause_age + cause_cohort).round(6).reset_index()
    projection['cohort_pct'] = pct_cohort
    projection = projection.set_index(['cohort_pct', 'year', 'age']).round().astype(int)
    projection = projection.reset_index().groupby(['cohort_pct', 'year']).sum()
    projection = projection.drop(columns = 'age')
    projection = projection.div(projection.sum(axis = 1), axis = 0)
    return projection


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS


def make_c1(people_forecast, params = z_tools.params):
    """
        Executes the functions in this module in sequence, generating population political
        leanings projections for an array of age vs. cohort influence assumptions.
    """
    people_forecast = simplify_people_forecast(people_forecast)
    vote = import_vote_data()
    vote = refine_vote_data(vote)
    cause_age = project_pure_age_scenario(people_forecast, vote)
    cause_cohort = project_pure_cohort_scenario(people_forecast, vote)
    vote_projections = [
        project_age_cohort_mix(cause_age, cause_cohort, pct_cohort=i) for i in params['cohort_pct']]
    vote_projections = pd.concat(vote_projections)
    return vote_projections


##########==========##########==========##########==========##########==========##########==========
## TEST CODE


if __name__ == '__main__':
    people_forecast = z_tools.execute_or_load_cache(b1_make_people_forecast.make_b1)[0]
    voter_forecast = make_c1(people_forecast = people_forecast)


##########==========##########==========##########==========##########==========##########==========
