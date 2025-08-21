## A file containing helper functions for loading and cleaning the data
# things to do:
# names not capitalized, leading/trailing spaces
# dates in multiple formats, including european and american
    # convert all to one format, determine how to handle euro dates when ambiguous
# emails contain diff formats, @/[at], some domains have one part or are "email"
# phones numbers have diff formats, dashes/slashes, int format, not real phone numbers (less than 10 digits)
# most addresses contain only street, assume correct format. malformed ones include a extra comma and one has apt number and one has the town name
# addresses contain diff street type format ex "st" and "street"
# some missing appointment_id
# appointment dates also in different formats, handle w generic helper

# start with some helper funcs to handle the data
# generalize when possible
# on FE, put a flag on patients missing large amounts of critical data

import csv
import re
import datetime

# define files and get fields from file? or assume a structure?
    # can choose to check if the assumed fields are the same as the derived ones

# define data cleaners

# define funcs to add to database