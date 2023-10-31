##########==========##########==========##########==========##########==========

## github.com/sjoshuam/life_expectancy
Repo creation date: 2023-10-07

#### Overview

Life expectancy is a commonly used health statistic.  It estimates how long a
person born today might live, assuming their their chances of dying match current
mortality statistics for every year of life. For example, imagine that 80% of 88
year-olds lived to see their 89th birthday, and 70% of 89 year-olds lived to see
their 90th birthday.  Using the life expectancy approach approach, we'd estimate
that that a given person, age 88, would have a 80% x 70% = 56% chance of living
to see their 90th birthday.

Life expectancy is typically expressed as the number of years that someone born
today might live. As of October 2023, the figure stands at 73.5 years for men,
and 79.3 years for women. However, the statistic is actually the oldest age at
which the newborn would have a 50% orbetter chance of being alive, if their
chances of mortality in each year match today's mortality rates.

This project uses the data underlying life expectancy to provide a little more
detail than that top-line figure.  It will generate a series of probability
density plots that reveal the most likely death year for people who are currently
of a specific year and gender.  The project code pipeline currently consists of
two scripts:

- 1_shape_data.py - uses the CDC's life tables to generate historgram coordinates
- 2_visualize.py  - generates a poster visualization

#### TODO

- [ ] 1_shape_data.py
    - [X] Download data (Aww... it's such an adorably tiny dataset!)
    - [X] import_data
    - [X] calculate_survival_for_all
        - [ ] Parallelize (not really needed, but good practice anyway)
    - [ ] Fill in doc string text

- [ ] 2_visualize.py
    - [X] Download data
    - [X] draw_background (use go.make_subplots(rows, cols))
    - [X] draw_life_chances
    - [X] add_text
    - [ ] draft explainer text
    - [ ] draft optimistic "What you can do"  living longer/better text
        - [ ] Research evidence-based longer life tips
        - [ ] Research evidence-based better life tips
    - [ ] Fill in doc string text

- [ ] Add new portfolio project deployment script to handle new format

#### Source

For more information on life expectancy, see the CDC's publications on the subject:

+ [US Life Tables, 2020](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-01.pdf)
+ [US State Life Tables, 2020](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-02.pdf)

##########==========##########==========##########==========##########==========
