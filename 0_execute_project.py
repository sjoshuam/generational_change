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
    for iter in ['html', 'css', 'png']:
        shutil.copy(f'out/generational_change.{iter}', f'../portfolio/p/generational_change.{iter}')
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
