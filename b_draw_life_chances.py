"""
    Module B: draw_life_chances draws an interactive area plot.  Plot shows the
    chances that an individual who was born in a given year will still be alive
    by a given age.
"""
##########==========##########==========##########==========##########==========
## INITIALIZE ENVIRONMENT

## libraries
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

##########==========##########==========##########==========##########==========
## DEFINE COMPONENT FUNCTIONS - DATA IMPORT AND TEXT ANNOTATIONS

def import_data():
    """
        Imports two files that contain key data for this project.

        survival_pct - for a person of a given birthyear and sex, calculates the
        percentage chances that the person will still be alive at a given age.
        Estimates are based on the method underlying life expectancy statistics.

        text.txt - text paragraphs that provide context for the life 
        expectancy statistics. Text includes 1) explanation of life expectany
        and this project's goals, 2) tips for longevity, and 3) tips for making
        good use of the time one has left.
    """
    xlsx = pd.read_excel(io = 'io/survival_pct.xlsx', index_col = [0, 1])
    with open('in/text.txt', 'rt') as conn:
        txt = ''.join(conn.readlines()).replace('\n', '<br>')
    txt = [i.strip() for i in txt.split('<block><br>') if len(i) > 0]
    
    return xlsx.sort_index(), txt


def add_text(text, rc, deg = 0):
    """
        Add a block of text to the figure.
        TODO: support textwrap, and multiple column placement
    """
    fig.add_annotation(
        row = rc[0], col = rc[1],
        arg = dict(
            x = 0.5, y = 0.5, text = text, textangle = deg, showarrow = False,
            font = dict(size = 12)
            )
        )
    fig.update_xaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])
    fig.update_yaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])
    return None

##########==========##########==========##########==========##########==========
## DEFINE COMPONENT FUNCTIONS - SHAPE DRAWING

def draw_background():
    """
        Draw basic plot layout
    """
    global fig
    fig = make_subplots(
        rows = 2, row_heights   = [4, 4],
        cols = 1, column_widths = [12],
    )
    fig.update_layout(
        template = 'plotly_dark',
        yaxis_range = [0, 1],
        xaxis_range = [2023, 2123]
        )
    fig.update_yaxes(tickformat=".0%")
    global fig_names
    fig_names = list()
    return None


def draw_life_chance_plot(birth_year, survival_pct):
    """
        Draws life expectancy percentage curves for men and women born in a
        given year.
    """
    for iter_sex in ['M', 'F']:
        fill, line_color = 'tozeroy', 'hsv(180, 50, 70)'
        if iter_sex == 'F': fill, line_color = 'tonexty', 'hsv(0, 50, 70)'
        fig.add_trace(
            row = 2, col = 1,
            trace = go.Scatter(
                x = survival_pct.loc[(iter_sex, birth_year)]['Age'].values,
                y = survival_pct.loc[(iter_sex, birth_year)]['Alive'].values,
                showlegend = False, 
                line_color = line_color,
                name = '{0}, Born {1}'.format(*(iter_sex, birth_year)),
                fill = fill,
                visible = birth_year == max(
                    survival_pct.index.get_level_values('Birthyear'))
                )
                )
        fig_names.append('{0}, Born {1}'.format(iter_sex, birth_year))
        fig.update_xaxes(row = 2, col = 1, range = [0, 90])
        fig.update_yaxes(row = 2, col = 1, range = [0, 1])
        fig.update_layout(hovermode = 'x')
    return None


def draw_slider_bar(birthyears):
    """
        Adds a slider bar to the figure, so that users can select different
        birth years and see life expectancy curves for currently living
        persons born that year.
    """
    steps = list()
    for iter_birthyear in birthyears:
        step_iter = dict(
            method = 'update',
            args = [
                {'visible':[i.endswith(str(iter_birthyear)) for i in fig_names]}
                ],
            label = iter_birthyear
        )
        steps.append(step_iter)

    sliders = [dict(
            active = len(birthyears),
            steps = steps,
            currentvalue = {'prefix':'Birth Year: '}
            )]
    fig.update_layout(sliders = sliders)
    return None

##########==========##########==========##########==========##########==========
## DEFINE TOP-LEVEL FUNCTION

def draw_life_chances(survival_pct):
    """
        Top-level function; executes the other functions in this module
    """

    ## draw background figure
    draw_background()

    ## find all valid birthyears
    birthyears = sorted(
        list(set(survival_pct.index.get_level_values('Birthyear'))))[::-1]
    
    ## iterate through birth years, drawing life chances
    for iter_birthyear in birthyears:
        draw_life_chance_plot(
            birth_year = iter_birthyear,
            survival_pct = survival_pct
            )
        
    ## add slider bar
    draw_slider_bar(birthyears = birthyears)

    ## add text panels
    add_text(text = ' '.join(text_blocks), rc = (1,1))

    ## export figure
    fig.write_html(
        'out/life_expectancy.html', default_width = 1200, default_height = 800)
    fig.write_image('out/life_expectancy.png', width = 1200, height = 800)

##########==========##########==========##########==========##########==========
## TEST FUNCTIONS AS NEEDED

if __name__ == '__main__':

    ## import data
    survival_pct, text_blocks = import_data()

    ## draw life chances plots
    draw_life_chances(survival_pct = survival_pct)


##########==========##########==========##########==========##########==========
