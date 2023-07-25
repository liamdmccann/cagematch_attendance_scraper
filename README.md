# cagematch_attendance_scraper
A script to scrape attendance figures from Cagematch.net.

# Venue Finder Cagematch Script (to be renamed)
This script:
- sends a request to CM via url variable
- returns page w. list of links
- scrapes list of links from page
- extracts to YAML

An example file from this process is available in new Korakuen show list.yaml.

# Cagematch Attendance Scraper

This script
- imports YAML files to give lists of shows
- builds a dictionary from each URL in relevant YAML file
- extracts relevant show info (name, attendance, venue, show name) into a dictionary
- writes show dictionaries out to CSV for processing

Using the Korakuen Hall shows.yaml and Korakuen_showlist demonstrates the scripts functionality when there are attendance values for every entry in the YAML. 
Using new Korakuen show list demonstrates script breaking when there are attendance values missing.
