# LinkGrabber - scraping script
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Functions](#functions)
* [Improvements for the future](#improvements-for-the-future)
* [Risks](#risks)

## General info
This script takes in a file named "keywords.txt" located in the same directory as the script itself, and returns two .csv files in the same directory:
- First one named "links.csv" containing first 10 links of google search results for each word located in "keywords.txt".
- Second one named "results.csv" containing all the words from "keywords.txt" associated with the number of google results they yield.

Currently the script accepts only keywords separated by space in one line.
Default number of links returned per keyword is 10.
	
## Technologies
Script is created with:
* Python 3.8
* Beautiful Soup package
* [googlesearch module](https://python-googlesearch.readthedocs.io/en/latest/)
	
## Setup
To run this script place it in the same folder as "keywords.txt"
```console
python linkGrabber.py
```

## Functions
### grab_links(site, word):
  Returns the list of links scrapped from the site with the use of search function from googlesearch module.

              Parameters:
                      site (str): String link
                      word (str): String

              Returns:
                      links_list (list): List of the links grabbed from google based on site and word
### grab_results(site, word)
  Returns the string of number of results when searching the google.

              Parameters:
                      site (str): String link
                      word (str): String

              Returns:
                      word: num_of_links (str): String of results from google based on site and word

## Improvements for the future
- User choice for naming the input and output files
- Ability to use the keyword files from outside the script directory
- Improved speed
- Possibility of using dedicated Google API for searching
- Ability to specify number of links being returned per keyword

## Risks
- Very high chance of getting banned by google for sending too many requests

