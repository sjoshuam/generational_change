##########==========##########==========##########==========##########==========##########==========
## HEADER

import z_tools, b1_make_people_forecast
import pandas as pd

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS

def lock_migration_rate(pf, migrant_rate = 1.05):
    """Simplifies projections to a single migration rate"""
    return pf.loc[(migrant_rate, )]


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS

##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    people_forecast = lock_migration_rate(
        z_tools.execute_or_load_cache(b1_make_people_forecast.make_b1)[0])
    print(people_forecast)


##########==========##########==========##########==========##########==========##########==========
