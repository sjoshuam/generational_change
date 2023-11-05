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
    fig = go.Figure()
    fig = fig.update_layout(
        plot_bgcolor  = params['light'], paper_bgcolor = params['light'],
        font = dict(size = 12, color = params['dark']),
        #yaxis = dict(range = [0, 1], tick0 = 0.1, dtick = 0.2, gridcolor = params['dark']),
        #xaxis = dict(range = params['years'], tick0 = min(params['years']) + 10, dtick = 20),
        )
    return fig


'''
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
'''


def write_html(div_list):
    """
        Assembles <div> sections into a single html file
    """
    header = '\n'.join([
        '<html>', '<header>',
        '\t<meta charset="utf-8" />',
        '\t<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>', 
        '\t<link rel="stylesheet" href="generational_change.css">',
        '</header>',
        '<body>'])
    footer = '\n'.join(['</body>', '</html>'])
    div_list = '\n'.join(div_list)
    html_file = '\n'.join([header, div_list, footer])
    open('out/generational_change.html', 'wt').write(html_file)
    shutil.copy('out/generational_change.html', '../portfolio/p/generational_change.html')
    shutil.copy('out/generational_change.css', '../portfolio/p/generational_change.css')
    #shutil.copy('out/generational_change.png', '../portfolio/p/generational_change.png')
    return html_file


##########==========##########==========##########==========##########==========##########==========
## TOP-LEVEL FUNCTIONS


def execute_project():

    ## generate container for div elements
    div_list = list()
    div_list = [
        '<a href="../index.html"> <div class="link_button">Return To Portfolio</div> </a>',
        '<div class="header"></div>', '<div class="header"></div>']

    ## draw life expectancy figure
    life_chances = a1_make_life_chances.make_life_chances()

    ## draw placeholders for forthcoming figures
    for iter in range(0, 3):
        div_list.append(a1_draw_life_chances.draw_life_chances(life_chances))
    div_list += ['<div class="txt"><p>EXPLAINER TEXT<br>Lorem Ipsom dolor sit amet.</p></div>'] * 2
    div_list.append(a1_draw_life_chances.draw_life_chances(life_chances))

    ## write html
    write_html(div_list)




##########==========##########==========##########==========##########==========##########==========
## EXECUTE PROJECT CODE

if __name__ == '__main__':
    execute_project()
