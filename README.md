# oscar_stats

Daily web-scraping of OSCAR class capacity data

## How it works

- Gets list of active CRNs from [gt-scheduler/crawler](https://github.com/gt-scheduler/crawler)
- For each CRN, get OSCAR page and extract section capacity info from table.
- Save to JSON, with format: `crn: [seats_capacity, seats_actual, seats_remaining, waitlist_capacity, waitlist_actual, waitlist_remaining, unix_timestamp]`
- Also save gt-scheduler data for reference (the gt-scheduler repo used to keep copies but they stopped so whatever)

## TODO
- Clean up code b/c its garbage
- Make different output folders for each semester
  - automate scraping of future semesters

## want to help?
- Make a script to transform data into usable `.csv` so ppl can make charts
  - For example, group CRNs together and add up totals for each class

