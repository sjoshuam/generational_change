"""
    TODO
"""

##########==========##########==========##########==========##########==========##########==========
## HEADER

## import libraries and modules
import b1_make_people_forecast, z_tools
import plotly.graph_objects as go

## TODO: Differentiate migrant rates by age?

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def set_up_figure(params = z_tools.params) -> go.Figure:
    """
        Purpose: Builds a basic plotly figure object
        Arguments:
            params: a parameters object with various control settings
        Returns: An empty plotly Figure object
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
        title = dict(
            text = 'Birth Cohort Population Percentage', xanchor = 'auto')
    )
    return fig


def draw_birth_decade_bars(migrant_rate, birth_decade, params = z_tools.params) -> list:
    """
        Purpose: Draws bars to indicate the population percentage of a given cohort in a given
            year.
        Arguments:
            birth_decade: data frame of population projections over time
            migrant_rate: assumed immigration rate over time, must correspond exactly to the 
                corresponding index in birth_decade.
            params: a parameters object with various control settings
        Returns: A list of plotly graphical elements
    """
    bd_subset = birth_decade.loc[(migrant_rate)].reset_index().set_index('birth_decade')
    trace_list = dict()
    for iter_index in bd_subset.index.unique()[::-1]:
        if iter_index == 0: iter_name = 'Other'
        else: iter_name = iter_index
        trace_list.update({
            (migrant_rate, iter_name):go.Bar(
                name = iter_name, width = 1.0,
                visible = migrant_rate == min(params['migrant_rate']),
                x = bd_subset.loc[iter_index, 'year'],
                y = bd_subset.loc[iter_index, 'pct'],
                marker = dict( color = params['cohort_colors'][iter_name] )
                )
            })
    return trace_list


def draw_slider(registry: list[tuple], params = z_tools.params):
    """
        Purpose: Adds an appropriate slider bar to the plotly figure
        Arguments:
            registry: a registry of names for the figures generated in draw_birth_decade_bars()
            params: a parameters object with various control settings
        Returns: A plotly slider object suitable for incorporation into a plotly Figure
    """

    ## generate visible instructions for each slider element
    steps = []
    for iter_steps in params['migrant_rate']:
        steps.append(
            dict(
                method = 'update',
                args = [{
                    'visible': [j[0] == iter_steps for j in registry]
                    }],
                label = str(round((iter_steps - 1) * 100)) + '%'
                )
            )
        
    ## package as a sider object
    sliders = [dict(
        active = params['migrant_rate'].index(1.15),
        steps = steps,
        currentvalue = {'prefix': 'Lifetime Migration Rate: '}
        )]
    
    return sliders

##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS

def draw_b1(birth_decade, params = z_tools.params):
    """
        Purpose: Draw population projections over time, showing the size of each birth decade
            cohort in each year.
        Arguments:
            birth_decade: data frame of population projections over time
        Returns: html code to display population projections as a stacked bar plot for years x
            population percentage
    """

    ## set up useful objects
    fig = set_up_figure()
    fig_registry = []

    ## append bar objects
    for iter_migrant in z_tools.params['migrant_rate']:
        trace_list = draw_birth_decade_bars(migrant_rate= iter_migrant, birth_decade= birth_decade)
        fig_registry.extend(trace_list.keys())
        fig = fig.add_traces(data = list(trace_list.values()))

    ## tie object visibility into a slider bar
    fig.update_layout(sliders = draw_slider(fig_registry))

    ## export objects to disk
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
