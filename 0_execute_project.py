"""
    Executes the life expectancy project
"""

##########==========##########==========##########==========##########==========
## IMPORT MODULES
import a_shape_data, b_draw_life_chances

##########==========##########==========##########==========##########==========
## DEFINE PROJECT-LEVEL FUNCTION

def execute_life_expectancy_project():
    a_shape_data.shape_data()
    b_draw_life_chances.draw_life_chances()


##########==========##########==========##########==========##########==========
## EXECUTE PROJECT

if __name__ == '__main__':
    execute_life_expectancy_project()

##########==========##########==========##########==========##########==========
