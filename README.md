##########==========##########==========##########==========##########==========##########==========

## github.com/sjoshuam/generational_change
Repo creation date: 2023-10-07
Rescoped: 2023-11-04

#### Overview

This project projects how the balance of economic and political power amoung
different generations of Americans may shift over the coming decades, based
on life expectancy.  The end product will be a 2 row x 3 column html data
display.

|       |Col. A |Col. B |Col. C |
|:-     |:-     |:-     |:-     |
|Row 1  |A1     |B1     |C1     |
|Row 2  |A2     |B2     |C2     |

Cells:

- Figure Cells
  - A1 - Life expectancy figure with birthyear slider
  - B1 – Population projection figure with birth vs immigration rate slider
  - C1 – Wealth projection figure with wealth rate slider
  - C2 – Voting projection figure with age vs cohort slider
- Text Cells
- A2 – Project explainer text
- B2 – Figure explainer texts

#### TODO

- [X] A1 Life Expectancy Figure with Birthyear Slider 
  - [X] a1_make_life_chances.py
  - [X] a1_draw_life_chances.py
- [ ] B1 Population Projection Figure with Migration Rate Slide
  - [X] b1_make_people_forecast.py
  - [ ] b1_draw_people_forecast.py
- [ ] C1 Wealth Projection Figure with Wealth Rate Slider
  - [ ] c1_make_wealth_forecast.py
  - [ ] c1_draw_wealth_forecast.py
- [ ] C2 Voting Projection Figure with Age/Cohort Slider
  - [ ] c2_make_voting_forecast.py
  - [ ] c2_draw_voting_forecast.py
- [ ] A2/B2 Explainer Text
  - [X] a2_do_project_text.py
  - [ ] project_text.txt
- [ ] Execute the Project
  - [ ] 0_execute_project.py
    - [X] Figure intitiator/writer code
    - [ ] Module executors
  - [ ] 1_tools.py
    - [X] parallelization tools
    - [ ] caching tools
  - [ ] Resolve leftover TODO in project files

#### Source

###### A1 Life Expectancy

[US CDC: Life Tables (2020)](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-01.pdf)

###### B1 Population Forecast

[US Census: Projected Population](https://www.census.gov/data/tables/2017/demo/popproj/2017-summary-tables.html)

[US Census: Immigration x Age Rates](https://www2.census.gov/programs-surveys/popproj/technical-documentation/methodology/methodstatement17.pdf)

###### C1 Wealth Projection

[US FRB: Age x Net Worth Table (2023)](https://www.federalreserve.gov/publications/files/scf23.pdf)

###### C2 Voting Projection

[ANES: Age x Party Table (2020)](https://sda.berkeley.edu/sdaweb/analysis/exec?formid=tbf&sdaprog=tables&dataset=nes2020full&sec508=false&row=V201507x&column=V201200&weightlist=V200010b&rowpct=on&design=complex&cflevel=95&weightedn=on&color=on&ch_type=stackedbar&ch_color=yes&ch_width=600&ch_height=400&ch_orientation=vertical&ch_effects=use2D&decpcts=1&decse=1&decdeft=3&decwn=1&decstats=2&csvformat=no&csvfilename=tables.csv)

##########==========##########==========##########==========##########==========##########==========
