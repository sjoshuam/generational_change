"""
    TODO: module description
"""

##########==========##########==========##########==========##########==========
## INITIALIZE ENVIRONMENT

## libraries
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## parameters
"""
    MANUAL PARAMETERS

    AUTOMATICALLY GENERATED PARAMETERS

"""

params = {}

##########==========##########==========##########==========##########==========
## DEFINE BASIC DRAWING FUNCTIONS


def import_data():
    """
        X
    """
    ## 
    xlsx = pd.read_excel(io = 'io/survival_pct.xlsx', index_col = [0, 1])
    with open('in/text.txt', 'rt') as conn:
        txt = ''.join(conn.readlines()).replace('\n', '<br>')
    txt = [i.strip() for i in txt.split('<block><br>') if len(i) > 0]
    
    return xlsx.sort_index(), txt


def draw_background():
    """
        Draw basic plot layout
    """
    global fig
    fig = make_subplots(
        rows = 6, row_heights   = [2.2, 0.2, 1.4, 1.4, 1.4, 1.4],
        cols = 4, column_widths = [0.2, 5.8, 0.2, 5.8],
    )
    fig.update_layout(
        template = 'plotly_dark',
        yaxis_range = [0, 1],
        xaxis_range = [2023, 2123]
        )
    fig.update_yaxes(tickformat=".0%")


def draw_life_chances(idx, rc, sc):
    """
        TODO
    """
    ## unpack coordinates into polygon
    x = sc.loc[idx]['Age'].values
    y = sc.loc[idx]['Alive'].values

    xx = np.append(x, x[::-1])
    yy = np.append(y, y * 0)

    ## draw life chances polygon
    fig.add_trace(
        row = rc[0], col = rc[1],
        trace = go.Scatter(
            x = xx, y = yy, fill = 'toself',
            showlegend = False, 
            line_color = 'hsv(150, 50, 70)',
            name = ''
        )
    )
    fig.add_trace(
        row = rc[0], col = rc[1],
        trace = go.Scatter(
            x = x, y = y,
            showlegend = False, 
            line_color = 'hsv(150, 50, 70)',
            name = 'Still Alive'
        )
    )
    fig.update_xaxes(row = rc[0], col = rc[1], range = [0, 100])
    fig.update_layout(hovermode = 'x')


def add_text(text, rc, deg = 0):
    fig.add_annotation(
        row = rc[0], col = rc[1],
        arg = dict(
            x = 0.5, y = 0.5, text = text, textangle = deg, showarrow = False,
            font = dict(size = 12)
            )
        )
    fig.update_xaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])
    fig.update_yaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])


##########==========##########==========##########==========##########==========
## DEFINE COMPOSITE DRAWING FUNCTIONS


def draw_life_chance_series(sex, col, survival_pct):
    birthyear = sorted(
        list(set(survival_pct.index.get_level_values('Birthyear'))))[::-1]
    
    ## iterate through birth years
    for iter_birthyear in birthyear:
        idx = birthyear.index(iter_birthyear) + 3

        ## draw life chance charts
        draw_life_chances((sex, iter_birthyear), (idx, col), survival_pct)

        ## draw life chance labels
        the_text = '<br>'.join(['<b>Age Now:<br>{0}yrs</b>'])
        the_text = the_text.format(
            pd.Timestamp.now().year - iter_birthyear
            )
        add_text(the_text, (idx, col - 1), deg = 270)


##########==========##########==========##########==========##########==========
## EXECUTE FUNCTIONS

if __name__ == '__main__':

    ## import data
    survival_pct, text_blocks = import_data()
    print(text_blocks)

    ## draw background figure
    draw_background()

    ## draw life chances plots
    add_text(text = '<b>Gender: Male</b>', rc = (2, 2))
    draw_life_chance_series('M', 2, survival_pct)
    add_text(text = '<b>Gender: Female</b>', rc = (2, 4))
    draw_life_chance_series('F', 4, survival_pct)

    ## add text panels
    add_text(text = text_blocks[0], rc = (1,2))
    add_text(text = text_blocks[1], rc = (1,4))

    ## write figure to disk
    fig.write_html(
        'out/life_expectancy.html', default_width = 1200, default_height = 800)
    fig.write_image('out/life_expectancy.png', width = 1200, height = 800)

##########==========##########==========##########==========##########==========
