"""
    This is the top-level executable python file for this project.  All other code is called though
    it.  Project generates a file called generational_change.html, which is a six-panel web page
    that walks through a highly simplified model of generational change and its potential effect
    on US presidential voting.  It calls eight module scripts:

    - a1_make_life_chances, a1_draw_life_chances: Life expectancy calculations and figures
    - b1_make_people_forecast, b1_draw_people_forecast: Population size forecasts by birth decade
    - c1_make_voter_forecast, c1_draw_voter_forecast: US presidential vote forecasts
    - a2_do_project_text: Explanatory text for a1, b1, c1
    - z_tools: Utility code for parallel processing, plus control parameters

"""
##########==========##########==========##########==========##########==========##########==========
## INITIALIZATION

## temporarily suppress panda's future warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
if __name__ == '__main__': print('\nNOTE: FUTURE WARNINGS ARE CURRENTLY BEING SURPRESSED')

## import libraries
import shutil
import a1_make_life_chances, a1_draw_life_chances
import b1_make_people_forecast, b1_draw_people_forecast
import c1_make_voter_forecast, c1_draw_voter_forecast

##########==========##########==========##########==========##########==========##########==========
## COMPONENT FUNCTIONS


def write_html(div_list: list) -> str:
    """
        This function packages a list of visualizations (coded as html div sections) together as
        one coherent web page.  It also copies files into the portfolio repository, so that
        the updated files will upload to the github.io webpage.
    """
    header = '\n'.join([
        '<html>', '<header>',
        '\t<meta charset="utf-8" />',
        '\t<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
        '\t<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Quicksand">',
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
        Executes the code from all project modules in sequence, running the project from start
        to finish.
    """
    ## pass css file to outputs
    shutil.copyfile('in/generational_change.css', 'out/generational_change.css')

    ## generate container for div elements
    div_list = list()
    div_list = [
        '<a href="../index.html"> <div class="link_button">Return To Portfolio</div> </a>',
        '<div class="header"></div>', '<div class="header"></div>']
    
    ## project intro text
    div_list.append('\n'.join(open('in/a0_text.html', 'rt').readlines()))

    ## a1 draw life expectancy figure
    life_chances = a1_make_life_chances.make_a1()
    div_list.append(a1_draw_life_chances.draw_a1(life_chances))

    ## b1 draw birth decade figure
    people_forecast, birth_decade = b1_make_people_forecast.make_b1()
    div_list.append(b1_draw_people_forecast.draw_b1(birth_decade))

    ## c1 draw vote projection figure
    voter_forecast = c1_make_voter_forecast.make_c1(people_forecast = people_forecast)
    div_list.append(c1_draw_voter_forecast.draw_c1(voter_forecast = voter_forecast))

    ###  panel explanation text
    div_list.append('\n'.join(open('in/a2_text.html', 'rt').readlines()))

    ## write html
    write_html(div_list)


##########==========##########==========##########==========##########==========##########==========
## EXECUTE PROJECT CODE

if __name__ == '__main__':
    execute_project()
