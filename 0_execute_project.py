"""
    TODO:
"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION


## import libraries
import shutil
import a1_make_life_chances, a1_draw_life_chances
import b1_make_people_forecast, b1_draw_people_forecast
import c1_make_voter_forecast #,c1_draw_voter_forecase
import a2_do_project_text

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
    """
        TODO: FILL IN FINAL DISCRIPTION AT THE END
    """

    ## generate container for div elements
    div_list = list()
    div_list = [
        '<a href="../index.html"> <div class="link_button">Return To Portfolio</div> </a>',
        '<div class="header"></div>', '<div class="header"></div>']

    ## a1 draw life expectancy figure
    life_chances = a1_make_life_chances.make_a1()
    div_list.append(a1_draw_life_chances.draw_a1(life_chances))

    ## b1 draw birth decade figure
    people_forecast, birth_decade = b1_make_people_forecast.make_b1()
    div_list.append(b1_draw_people_forecast.draw_b1(birth_decade))

    ## c1 draw vote projection figure
    voter_forecast = c1_make_voter_forecast.make_c1(people_forecast = people_forecast)
    div_list.append(a1_draw_life_chances.draw_a1(life_chances))  ## PLACEHOLDER

    ##  a2/b2 draw project text
    project_text = a2_do_project_text.make()
    for iter_key in project_text.keys():
        div_list.append(a2_do_project_text.draw((0.5, 0.5), project_text[iter_key]))

    ## write html
    write_html(div_list)


##########==========##########==========##########==========##########==========##########==========
## EXECUTE PROJECT CODE

if __name__ == '__main__':
    execute_project()
