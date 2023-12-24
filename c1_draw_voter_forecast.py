"""
    TODO:
"""

##########==========##########==========##########==========##########==========##########==========
## HEADER
import os
import z_tools, c1_make_voter_forecast, b1_make_people_forecast
import pandas as pd
import plotly.graph_objects as go

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def set_up_figure(params = z_tools.params) -> go.Figure:
    """
        Purpose: Builds a basic plotly figure object
        Arguments:
            params: a parameters object with various control settings
        Returns: An empty plotly Figure object
    """
    m = params['margin']
    fig = go.Figure()
    fig = fig.update_layout(
        plot_bgcolor = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        xaxis = dict(
            range = [min(params['proj_time_window']), max(params['proj_time_window'])],
            tick0 = min(params['proj_time_window']) + 5, dtick = 10, gridcolor = params['dark']
            ),
        yaxis = dict(
            range = [0, 1], tickformat = '0%',
            tick0 = 0.1, dtick = 0.2, gridcolor = params['dark']
            ),
        margin = go.layout.Margin(t = m, l = m, b = m, r = m)
    )
    return fig


def draw_voter_blocs(
        voter_forecast: pd.DataFrame, cohort_pct: float, params = z_tools.params) -> go.Scatter:
    """
        TODO:
    """
    x_coord = voter_forecast.loc[cohort_pct].index.values
    lean_name = {'con': 'Conserv.', 'lib': 'Liberal', 'either': 'Con. + Lib.'}
    trace_list = dict()
    dash_type = 'solid'
    for iter_lean in lean_name.keys():
        if iter_lean == 'either': dash_type = 'dot'
        trace_list.update({
            str(int(cohort_pct * 100)) + '% ' + lean_name[iter_lean]: go.Scatter(
                x = x_coord, y = voter_forecast.loc[cohort_pct, iter_lean].round(3),
                showlegend = True,
                line_color = params['lean_colors'][iter_lean],
                visible = cohort_pct == 0.5,
                name = lean_name[iter_lean],
                line = dict(width = 3, dash = dash_type)
                )})
    return trace_list


def draw_slider_bar(trace_list):
    """
        TODO:
    """
    cohort_pct_list = sorted(list(set([i.split(' ')[0] for i in trace_list.keys()])))
    steps = list()
    for iter_pct in cohort_pct_list:
        step_iter = dict(
            method = 'update',
            args = [{'visible':[i.startswith(iter_pct) for i in trace_list.keys()]}],
            label = iter_pct
        )
        steps.append(step_iter)

    sliders = [dict(
            active = cohort_pct_list.index('50%'),
            steps = steps,
            currentvalue = {'prefix':'Political Lean Attributable To Cohort: '}
            )]
    
    return sliders


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTION

def draw_c1(voter_forecast):
    """
        TODO:
    """
    ## set up basic figure
    fig = set_up_figure()

    ## iteratively generate traces
    trace_list = dict()
    for iter_pct in set(voter_forecast.index.get_level_values('cohort_pct')):
        trace_list.update(draw_voter_blocs(voter_forecast = voter_forecast, cohort_pct = iter_pct))
    fig = fig.add_traces([trace_list[i] for i in trace_list.keys()])
    fig = fig.update_layout(
        sliders = draw_slider_bar(trace_list)
        )
    fig.write_html(file = 'out/c1_voter_forecast.html',full_html = True, include_plotlyjs = True)
    fig.write_html(file = 'out/c1_voter_forecast.div',full_html = False, include_plotlyjs = False)
    div = open('out/c1_voter_forecast.div', 'rt').read()
    os.remove('out/c1_voter_forecast.div')
    return div


##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    people_forecast = z_tools.execute_or_load_cache(b1_make_people_forecast.make_b1)[0]
    voter_forecast = z_tools.execute_or_load_cache(
        c1_make_voter_forecast.make_c1, people_forecast = people_forecast)
    div = draw_c1(voter_forecast)

##########==========##########==========##########==========##########==========##########==========
