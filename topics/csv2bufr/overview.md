# csv2bufr training

## Prerequisites
- Basic Linux command line tools, including use of a text editor
- Basic knowledge of BUFR, including knowledge of BUFR tables B (BUFR elements) and D (BUFR sequences)
- Knowledge of the formatting requirements of WIGOS identifiers

## Exercises

1. Create a simple csv2bufr mapping template using only BUFR elements and convert a test file to BUFR.
2. As exercise 1, but replacing the individual BUFR elements with BUFR sequences where applicable. 
3. Customise the mapping template to use a CSV data file with different column names.
4. Create a sequence for the reporting of hourly data according to GBON requirements.

Depending on progress and time available, two additional topics can be included:

5. Unit conversions: Celsius -> Kelvin, hectopascals to pascals.
6. Quality control, specifying valid ranges.

Each exercise is intended to be a small task (5 - 10 minutes) reinforcing the training materials presented
and to give the students the basic building blocks for encoding data to BUFR. Students should also come away with 
knowledge of further training resources and where to find further information. 

## Learning outcomes

By the end of the session students should be able to use the tools provided by csv2bufr to
- Create a BUFR mapping file and understand the basic structure
- Understand the links between the mapping file and the data in their CSV files. 
- Customise the BUFR mapping file (and/or input CSV) to apply to their CSV date.
- Succesfully convert their data to the recommended BUFR sequence to meet GBON requirements.

## File / training material structure

Each exercise is packaged in its own directory containing the following:

- Instructions on the task (``./instructions.md``)
- Example / training data (``./data/``)
- Example solution (``./solution/solution.md``, ``./solution/output/``)

## Further reading

Links to follow