##########==========##########==========##########==========##########==========

## github.com/sjoshuam/life_expectancy

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

#### Poster Layout

|       |      |       |       |
|:-     |:-    |:-     |:-     |
|(a)    |(b)   |40F    |40M    |
|00F    |00M   |50F    |50M    |
|10F    |10M   |60F    |60M    |
|20F    |20M   |70F    |70M    |
|30F    |30M   |80F    |80M    |

- (a) Project summary text
- (b) Long and fulfilling life, tips and links
- Other cells - year x mortality chance area plot

#### TODO

- [ ] 1_shape_data.py
    - [X] Download data
    - [ ] Outline work (add checkboxes)
- [ ] 1_shape_data.py
    - [X] Download data
    - [ ] Outline work (add checkboxes)
    - [ ] Draw cell A text
    - [ ] Draw cell B text

#### Source

For more information on life expectancy, see the CDC's publications on the subject:

[US Life Tables, 2020](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-01.pdf)
[US State Life Tables, 2020](https://www.cdc.gov/nchs/data/nvsr/nvsr71/nvsr71-02.pdf)

##########==========##########==========##########==========##########==========
