"""
    TODO
"""
##########==========##########==========##########==========##########==========##########==========
## HEADER


import b1_make_people_forecast, z_tools
import plotly.graph_objects as go
import pandas as pd

print('NEXT TODO: iterate throough visibility, then add slider bar')

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def set_up_figure(birth_decade, params):
    """
        TODO
    """
    fig = go.Figure()
    fig = fig.update_layout(
        plot_bgcolor = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        xaxis = dict(
            range = [min(params['bar_time_window']), max(params['bar_time_window'])],
            tick0 = min(params['bar_time_window']) + 5, dtick = 10, gridcolor = params['dark']
            ),
        yaxis = dict(
            range = [0, 1], tickformat = '0%',
            tick0 = 0.1, dtick = 0.2, gridcolor = params['dark']
            ),
        barmode = 'stack',
        title = dict(text = '•' + ' ' * 10 + 'Birth Cohort Population Percentage', xanchor = 'auto')
    )
    return fig

def draw_birth_decade_bars(migrant_rate, birth_decade):
    bd_subset = birth_decade.loc[(1.05)].reset_index().set_index('birth_decade')
    trace_list = list()
    for iter_index in bd_subset.index.unique():
        if iter_index == 0: iter_name = 'Other'
        else: iter_name = iter_index
        trace_list.append(
            go.Bar(name = iter_name, width = 1,
                   x = bd_subset.loc[iter_index, 'year'], y = bd_subset.loc[iter_index, 'pct'])
        )
    return trace_list


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS

def draw_b1(birth_decade, params = z_tools.params):
    """
        TODO
    """
    fig = set_up_figure(birth_decade = birth_decade, params = params)
    trace_list = draw_birth_decade_bars(migrant_rate = 1.05, birth_decade = birth_decade)

    fig = fig.add_traces(data = trace_list)

    fig.write_html(file = 'out/b1_people_forecast.html',full_html = True, include_plotlyjs = True)
    fig.write_html(file = 'out/b1_people_forecast.div',full_html = False, include_plotlyjs = False)
    div = open('out/b1_people_forecast.div', 'rt').read()
    return div

##########==========##########==========##########==========##########==========##########==========
## TEST CODE

if __name__ == '__main__':
    birth_decade = z_tools.execute_or_load_cache(b1_make_people_forecast.make_b1)[1]
    div = draw_b1(birth_decade)


##########==========##########==========##########==========##########==========##########==========
