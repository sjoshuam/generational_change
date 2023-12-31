"""
    TODO:
"""

##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## imports
import os
import plotly.graph_objects as go
import a1_make_life_chances, z_tools


##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def set_up_figure(life_changes, params = z_tools.params):
    """
        Set up a basic figure
    """
    m = params['margin']
    year_range = life_changes['Age'].agg({'min':min, 'max':max}).values
    fig = go.Figure()
    fig = fig.update_layout(
        plot_bgcolor  = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        yaxis = dict(range = [0, 1], tick0 = 0.1, dtick = 0.2, gridcolor = params['dark'],
            tickformat = '0%'),
        xaxis = dict(
            range= year_range, tick0= min(year_range) + 10, dtick= 20, gridcolor= params['dark']),
        margin = go.layout.Margin(t = m, l = m, b = m, r = m)
        )
    return fig


def draw_chances_from_birth_year(birth_year, life_chances):
    """
        Projects a survival probably curve for a given birth year, starting with the current year
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

def draw_slider_bar(trace_list, life_chances):
    """
        Adds a slider bar to the figure, so that users can select different
        birth years and see life expectancy curves for currently living
        persons born that year.
    """
    birth_years = set(life_chances.index.get_level_values('Birthyear'))
    steps = list()
    for iter_birthyear in birth_years:
        step_iter = dict(
            method = 'update',
            args = [
                {'visible':[i.endswith(str(iter_birthyear)) for i in trace_list.keys()]}
                ],
            label = iter_birthyear
        )
        steps.append(step_iter)

    sliders = [dict(
            active = len(birth_years) - 1,
            steps = steps,
            currentvalue = {'prefix':'Birth Year: '}
            )]
    
    return sliders


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


def draw_a1(life_chances):
    """
        Generate html div code for life chances
    """
    fig = set_up_figure(life_chances)
    trace_list = iterate_all_life_chances(life_chances)
    fig = fig.add_traces([trace_list[i] for i in trace_list.keys()])
    fig = fig.update_layout(
        sliders = draw_slider_bar(trace_list, life_chances),
        )
    fig.write_html(file = 'out/a1_life_chances.html',full_html = True, include_plotlyjs = True)
    fig.write_html(file = 'out/a1_life_chances.div',full_html = False, include_plotlyjs = False)
    div = open('out/a1_life_chances.div', 'rt').read()
    os.remove('out/a1_life_chances.div')
    return div


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':

    ## set up test
    life_chances = z_tools.execute_or_load_cache(a1_make_life_chances.make_a1)
    life_chances_drawn = draw_a1(life_chances)


##########==========##########==========##########==========##########==========##########==========
