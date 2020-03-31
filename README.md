# Covid-19-Measures-and-Events

## COVID-19 Measures and Events Timeline By Country taken from Wikipedia

The crawler connects to Wikipedia API and fetches data for 'Reactions and measures outside mainland China' section.
Then it tries to identify country and date and puts them in a csv format.

Usage example:
```bash
python3.8 covidMeasuresWikiCrawler.py March 2020
```

Tested with python3.8

Currently this covers only measures outside China sections.
Sample wikipedia page can be found [here](https://en.wikipedia.org/wiki/Timeline_of_the_2019%E2%80%9320_coronavirus_pandemic_in_March_2020#Reactions_and_measures_outside_mainland_China)

The data can be used for analytical purposes to combine with active case amounts to see the effects of measures on the growth of new infections

Terms of Use:
I do not guarantee any accuracy, liability or warranty for use or merchantibility for the script and the data.   
