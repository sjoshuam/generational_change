##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## imports
import re
import pandas as pd
import plotly.graph_objects as go
from plotly import offline

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS

def draw_chances_from_birth_year(birth_year, life_chances):
    """
    """
    trace_list = {
        'Life Chances: M ' + str(birth_year): go.Scatter(
            x = life_chances.loc[('M', birth_year)]['Age'].values,
            y = life_chances.loc[('M', birth_year)]['Alive'].values,
            showlegend = False, fill = 'tozeroy', line_color = 'hsv(180,80,80)',
            visible = birth_year == max(life_chances.index.get_level_values('Birthyear')),
            name = 'M ' + str(birth_year)
            ),
        'Life Chances: F ' + str(birth_year): go.Scatter(
            x = life_chances.loc[('F', birth_year)]['Age'].values,
            y = life_chances.loc[('F', birth_year)]['Alive'].values,
            showlegend = False, fill = 'tonexty', line_color = 'hsv(0,80,80)',
            visible = birth_year == max(life_chances.index.get_level_values('Birthyear')),
            name = 'F ' + str(birth_year)
            )
    }
    return trace_list

##########==========##########==========##########==========##########==========##########==========
## MID-LEVEL ITERATURES


def iterate_all_life_chances(life_chances):
    """
        Iterate draw_chances_from_birth_year() for all birth years
    """
    trace_list = dict()
    for iter_year in set(life_chances.index.get_level_values('Birthyear')):
        trace_list.update(draw_chances_from_birth_year(iter_year, life_chances))
    return trace_list


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION


def draw_life_chances(life_chances):
    """
        Generate html div code for life chances
    """
    fig = go.Figure()

    trace_list = iterate_all_life_chances(life_chances)
    fig = fig.add_traces([trace_list[i] for i in trace_list.keys()])
    div = offline.plot(fig, include_plotlyjs = False, output_type = 'div')
    open('out/life_chances.div', 'wt').write(div)
    return div


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':

    ## set up test
    life_chances = pd.read_excel('io/life_chances.xlsx', index_col = [0,1])
    fig = go.Figure()
    fig = fig.update_layout(template = 'plotly_dark')
    life_chances_drawn = draw_life_chances(fig, life_chances)


##########==========##########==========##########==========##########==========##########==========
