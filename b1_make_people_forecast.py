##########==========##########==========##########==========##########==========##########==========
## INITIALIZE

import pandas as pd

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def import_data(year_range = [1930, 2100]) -> pd.DataFrame:
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
    future_birth['SEX'] = future_birth['SEX'].replace({0:'birth_all', 1:'birth_male', 2:'birth_fem'})
    future_birth = future_birth.loc[(future_birth['ORIGIN'] + future_birth['RACE']) == 0]
    future_birth = future_birth.drop(columns = ['ORIGIN', 'RACE']).pivot_table(index = 'year',
        columns = 'SEX', values = ['POP_0', 'people'], aggfunc = sum).reset_index()
    future_birth.columns.name = None
    future_birth = pd.concat(
        [future_birth[['year']], future_birth[('POP_0')], future_birth[('people', 'birth_all')]],
        axis = 1).rename(columns = {('year', ''): 'year', ('people', 'birth_all'): 'people'})
    future_birth['male_pct'] = future_birth['birth_male'] / future_birth['birth_all']
    
    ## fuse datasets and standardized
    birth = pd.concat([historic_birth, future_birth], axis = 0).sort_values('year')
    index = pd.DataFrame({'year': list(range(min(year_range), max(year_range)+ 1))})
    birth = index.merge(birth, how = 'left', on = 'year').copy()
    birth = birth.merge(historic_people.rename(columns= {'people': 'x'}), how= 'left', on= 'year')
    birth.loc[birth['people'].isna(), 'people'] = birth.loc[birth['people'].isna(), 'x']
    birth = birth.drop(columns = 'x')

    return birth


def interpolate_missing_data(birth):
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
    idx = birth['birth_male'].isna()
    birth.loc[idx, 'birth_male'] = birth.loc[idx, 'male_pct'] * birth.loc[idx, 'birth_all']
    birth.loc[idx, 'birth_fem'] = birth.loc[idx, 'birth_all']  - birth.loc[idx, 'birth_male']

    ## clean up number types and precision
    birth = birth.astype({i:int for i in ['birth_male', 'birth_fem', 'birth_all', 'people']})
    birth = birth.round(6)

    return birth


def export_birth(birth):
    birth.set_index('year').to_excel('io/b1_birth.xlsx')


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION


def make_people_forecast():
    """
        TODO
    """
    birth = import_data()
    birth = interpolate_missing_data(birth)
    export_birth(birth)  ## TODO: remove this after more dev is done
    return birth


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    birth = make_people_forecast()
    

##########==========##########==========##########==========##########==========##########==========
