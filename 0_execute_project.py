"""
    X
"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION


## import libraries
import shutil
import a1_make_life_chances, a1_draw_life_chances, a2_do_project_text
import b1_make_people_forecast
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

    ## a1 draw life expectancy figure
    life_chances = a1_make_life_chances.make()
    div_list.append(a1_draw_life_chances.draw(life_chances))

    ## b1 draw birth decade figure IN PROGRESS
    people_forecaset, birth_decade_size = b1_make_people_forecast.make()
    div_list.append(a1_draw_life_chances.draw(life_chances))  ## placeholder

    ## c1 PLACEHOLDER
    div_list.append(a1_draw_life_chances.draw(life_chances))  ## placeholder

    ##  a2/b2 draw project text
    project_text = a2_do_project_text.make()
    for iter_key in project_text.keys():
        div_list.append(a2_do_project_text.draw((0.5, 0.5), project_text[iter_key]))
    
    ## c2 PLACEHOLDER
    div_list.append(a1_draw_life_chances.draw(life_chances))  ## placeholder

    ## write html
    write_html(div_list)




##########==========##########==========##########==========##########==========##########==========
## EXECUTE PROJECT CODE

if __name__ == '__main__':
    execute_project()
