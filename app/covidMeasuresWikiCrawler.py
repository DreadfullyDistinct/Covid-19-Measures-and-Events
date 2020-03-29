import json
import urllib.request
import re
import csv
import sys
import time
import argparse
from datetime import datetime
from urllib.parse import quote_plus

parser = argparse.ArgumentParser()
parser.add_argument("month", help="specify the month for example: March")
parser.add_argument("year", help="specify the year for example: 2020")

args = parser.parse_args()
month = args.month
year = args.year


# Path for Timeline info of COVID-19 in wikipedia
wikiPath = 'https://en.wikipedia.org/w/api.php?action=parse&page=Timeline_of_the_2019%E2%80%9320_coronavirus_pandemic_in_'+quote_plus(month)+'_'+quote_plus(year)+'_&prop=wikitext&formatversion=2&format=json'

jsonResponse = urllib.request.urlopen(wikiPath).read().decode(encoding="utf-8", errors="ignore")

# Start of Reactions and Measures outside China Section
startSection = '== Reactions and measures outside mainland China =='
startSection = jsonResponse.find(startSection)

if startSection == -1:
    print("The page does not contain Measures. Check your parameters")
    sys.exit(0)

# Headings for Dates format
firstDate = '=== 1 %s ===' % (month)
firstDateSection = jsonResponse[startSection:].find(firstDate) + startSection

# Each Measure starts with a new line character and ends with a link reference
eventRegex = r"(?<=\\n)(.*?)(?=<ref)" 

# Date Headings have === Date === format
dateRegex = r"(?<=\=\=\=).*?(?=\=\=\=)"

# Fetch whole section with Reactions and measures
allEvents=jsonResponse[firstDateSection:]

# Get all Measures and remove link references etc
events = re.finditer(eventRegex, allEvents, re.MULTILINE)

# CSV output file
csvOutputFilename = '../csvOutput/Covid19MeasuresandEvents' + year + month + '.csv'

# Function to match Country name, who takes the measure

def matchCountry(row):

    i=0
    matches={}

    with open('../resources/country-keyword-list.csv', 'r', newline='') as f:

        thereader=csv.reader(f)

        for column in thereader:

            checkMatchCountry= re.search(column[0], row, re.IGNORECASE)
            
            if checkMatchCountry:

                # We found a country name in the text
                matches[i] = column[0]
                i+=1


            if len(column)>1 :

                checkMatchNationality =  re.search(column[1], row, re.IGNORECASE)

                if checkMatchNationality:

                    # We found a nationality name in the text
                    matches[i] = column[0]
                    i+=1

    if i==0:
        return 'Other'
    if i==1 :
        return matches[0]
    if i>1 :

        # We have several country names referenced in the sentence.
        # This part normally requires NLP and probably Spacy, to check who really the subject is
        # I just took the first word, as it is highly likely that the first menioned country is the one taking the measure in the sentence.

        return matches[0]

with open(csvOutputFilename, 'w', newline='') as f:
    
    thewriter = csv.writer(f)
    
    thewriter.writerow(['Date', 'Country','Event'])

    currentDate = re.search(dateRegex,firstDate).group() 
    for eventNum, event in enumerate(events, start=1):
    
        # A bit cleanup to remove special characters
        event = event.group()
        event = event.replace("[","")
        event = event.replace("]","")
        event = event.replace("\\n","")

        # Match the date
        datematch = re.search(dateRegex,event)
        if datematch:
            currentDate = datematch.group()
    
        # Lets cleanup the date from events, as it is already fetched in the csv
        event = re.sub(r"(\=\=\=).*?(\=\=\=)", '' , event)   
        
        # February 29 causes exception due to leap year. For now this is a dirty fix.
        try:
            currentDateISO8601 = datetime.strptime(currentDate.strip(), '%d %B')
            currentDateISO8601 = currentDateISO8601.strftime('2020-%m-%d')
        except:
            currentDateISO8601 = '2020-02-29'

        # Match the name of Country
        countryName = matchCountry(event)
        
        #Write to Csv and we are done
        thewriter.writerow([currentDateISO8601, countryName, event])
