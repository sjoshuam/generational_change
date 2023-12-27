##########==========##########==========##########==========##########==========##########==========

## github.com/sjoshuam/generational_change
Repo creation date: 2023-10-07
Rescoped: 2023-11-04

#### Overview

Project generates a file called generational_change.html, which is a six-panel web page
that walks through a highly simplified model of generational change and its potential effect
on political leanings in the US population.

#### TODO

- [X] A1 Life Expectancy Figure with Birthyear Slider 
  - [X] a1_make_life_chances.py
  - [X] a1_draw_life_chances.py
- [X] B1 Population Projection Figure with Migration Rate Slider
  - [X] b1_make_people_forecast.py
  - [X] b1_draw_people_forecast.py
- [X] C1 Political Lean Projection Figure with Age Versus Cohort Slider
  - [X] c1_make_voter_forecast.py
  - [X] c1_draw_voter_forecast.py
- [X] Explainer Text
  - [X] Project Introduction
  - [X] A1 Explanation Text
  - [X] B1 Explanation Text
  - [X] C1 Explanation Text
- [X] Execute the Project
  - [X] 0_execute_project.py
    - [X] Figure intitiator/writer code
    - [X] Module executors
  - [X] 1_tools.py
    - [X] parallelization tools
    - [X] caching tools
  - [ ] Polish project
    - [ ] Resolve leftover TODO in project files
    - [ ] Confirm all doc strings written
    - [ ] Proof read and polish text
    - [ ] Add project description to portfolio
    - [ ] Get feedback
    - [ ] Revised based on feedback

#### Source

###### A1 Life Expectancy

[US CDC: Life Tables (2020)](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-01.pdf)

###### B1 Population Forecast

[US Census: Projected Population](https://www.census.gov/data/tables/2017/demo/popproj/2017-summary-tables.html)

[US Census: Immigration x Age Rates](https://www2.census.gov/programs-surveys/popproj/technical-documentation/methodology/methodstatement17.pdf)

###### C1 Voting Projection

[ANES: Age x Party Table (2020)](https://sda.berkeley.edu/sdaweb/analysis/exec?formid=tbf&sdaprog=tables&dataset=nes2020full&sec508=false&row=V201507x&column=V201200&weightlist=V200010b&rowpct=on&design=complex&cflevel=95&weightedn=on&color=on&ch_type=stackedbar&ch_color=yes&ch_width=600&ch_height=400&ch_orientation=vertical&ch_effects=use2D&decpcts=1&decse=1&decdeft=3&decwn=1&decstats=2&csvformat=no&csvfilename=tables.csv)

##########==========##########==========##########==========##########==========##########==========
