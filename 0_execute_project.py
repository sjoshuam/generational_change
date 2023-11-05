"""
    X
"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION


## import libraries
import shutil
import a1_make_life_chances, a1_draw_life_chances
from plotly.subplots import make_subplots
import plotly.graph_objects as go


## define parameters
params = {
    'years': [2023, 2123],
    'dark': '#663D14', 'light': '#FFF9F2',
}


##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS
## colors: 'hsv(30,5,100)' '#FFF9F2' / 'hsv(30,80,40)' '#663D14'


def initialize_figure(params = params):
    """
        Initialize basic plotly object (global)
    """
    fig = make_subplots(rows = 3, row_heights = [0.2,3.9,3.9], cols = 3, column_widths = [4,4,4])
    fig = fig.update_layout(
        plot_bgcolor  = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        #yaxis = dict(range = [0, 1], tick0 = 0.1, dtick = 0.2, gridcolor = params['dark']),
        #xaxis = dict(range = params['years'], tick0 = min(params['years']) + 10, dtick = 20),
        )
    return fig


def write_figure(fig, name = 'generational_change'):
    """
        Write figure to disk
    """
    in_file = 'out/' + name + '.html'
    out_file = '../portfolio/' + name + '.html'
    fig.write_html(in_file, default_width = 1200, default_height = 800)
    fig.write_image(in_file.replace('.html', '.png'), width = 1200, height = 800)
    shutil.copyfile(in_file, out_file)
    shutil.copyfile(in_file.replace('.html', '.png'), out_file.replace('.html', '.png'))


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS


def execute_project():

    ## generate figure
    fig = initialize_figure()

    ## draw life expectancy figure
    life_chances = a1_make_life_chances.make_life_chances()
    life_chances_drawn = a1_draw_life_chances.draw_life_chances(fig, life_chances)
    for iter in life_chances_drawn.keys():
        fig.add_trace(row = 2, col = 1, trace = life_chances_drawn[iter])

    ## write figure to disk and propagate to portfolio
    write_figure(fig)


##########==========##########==========##########==========##########==========##########==========
## EXECUTE PROJECT CODE

if __name__ == '__main__':
    execute_project()
