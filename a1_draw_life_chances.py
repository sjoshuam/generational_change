##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## imports
import pandas as pd
import plotly.graph_objects as go

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS

def draw_chances_from_birth_year(birth_year, life_chances):
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
## TOP-LEVEL FUNCTION


def draw_life_chances(fig, life_chances):
    """
        Top-level function; executes the other functions in this module
    """
    trace_list = dict()
    for iter_year in set(life_chances.index.get_level_values('Birthyear')):
        trace_list.update(draw_chances_from_birth_year(iter_year, life_chances))
    return trace_list


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':

    ## set up test
    life_chances = pd.read_excel('io/life_chances.xlsx', index_col = [0,1])
    fig = go.Figure()
    fig = fig.update_layout(template = 'plotly_dark')

    ## 
    life_chances_drawn = draw_life_chances(fig, life_chances)

    ## view test results
    fig.add_traces([life_chances_drawn[i] for i in life_chances_drawn.keys()])
    fig.write_html('out/TEST.html', default_width = 1200, default_height = 800)

##########==========##########==========##########==========##########==========##########==========
