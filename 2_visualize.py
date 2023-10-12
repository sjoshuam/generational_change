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
    x = pd.read_excel(io = 'io/survival_pct.xlsx', index_col = [0, 1])
    return x.sort_index()


def draw_background():
    """
        Draw basic plot layout
    """
    global fig
    fig = make_subplots(
        rows = 5, row_heights   = [2, 1.5, 1.5, 1.5, 1.5],
        cols = 5, column_widths = [0.34, 0.33, 5.5, 0.33, 5.5],
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

    x = np.append(x, x[::-1])
    y = np.append(y, y * 0)

    ## draw life chances polygon
    fig.add_trace(
        row = rc[0], col = rc[1],
        trace = go.Scatter(
            x = x, y = y, fill = 'toself',
            showlegend = False
        )
    )
    fig.update_xaxes(row = rc[0], col = rc[1], range = [0, 100])

    ## return the 17th-83th percentile life expectancies
    return (
        x[y == min(y[y > 5/6])][0], 
        x[y == min(y[y > 1/6])][0]
        )


def add_text(text, rc):
    fig.add_annotation(
        row = rc[0], col = rc[1],
        arg = dict(
            x = 0.5, y = 0.5, text = text, textangle = 270, showarrow = False,
            font = dict(size = 12)
            )
        )
    fig.update_xaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])
    fig.update_yaxes(row = rc[0], col = rc[1], visible = False, range = [0,1])

def draw_note_lines():
    pass

##########==========##########==========##########==========##########==========
## DEFINE COMPOSITE DRAWING FUNCTIONS

def draw_life_chance_series(sex, col, survival_pct):
    birthyear = sorted(
        list(set(survival_pct.index.get_level_values('Birthyear'))))[::-1]
    
    ## iterate through birth years
    for iter_birthyear in birthyear:
        idx = birthyear.index(iter_birthyear) + 2

        ## draw life chance charts
        life_pct = draw_life_chances(
            (sex, iter_birthyear), (idx, col), survival_pct)

        ## draw life chance labels
        the_text = '<br><br>'.join([
            '<b>Final Age: {1}-{2}</b>'
        ])
        the_text = the_text.format(
            pd.Timestamp.now().year - iter_birthyear,
            min(life_pct),
            max(life_pct)
            )
        add_text(the_text, (idx, col - 1))




##########==========##########==========##########==========##########==========
## EXECUTE FUNCTIONS

if __name__ == '__main__':

    ## import data
    survival_pct = import_data()

    ## draw background figure
    draw_background()

    ## draw life chances plots
    draw_life_chance_series('M', 3, survival_pct)
    draw_life_chance_series('F', 5, survival_pct)

    ## write figure to disk
    fig.write_html('out/test.html')

##########==========##########==========##########==========##########==========
