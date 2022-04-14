# Module for tides 4/13/2022
#   Purpose: Scrape a field from a url and return the time and height for each daylight low tide.
#   inputs: One place name(city, state)
#   Outputs: time and height for each place name's daylight lowtide -> Field Output will be text(place name, time, height)
#   Assumptions: Python Interpreter is 3.8 in a virtual python environment using PyCharm IDE with pytest, lxml and requests libs installed in venv
#   Use: Import the getTidalInfo function(from tides import getTidalInfo),
#   then call the function with a string containing the place ... getTidalInfo('Some City, Some State')
#   Testing: Run "pytest -q tides.py" in top project directory

from lxml import html
import requests
import re


def getTidalInfo(place):
    # Accept a place name to lookup on with url:
    # if place fits format then make a request to url, return and format results
    # In case of empty(no places) input print a meaningful message and exit
    pat = re.compile('[\s,]')
    pat2 = re.compile('--')
    pat3 = re.compile('locations')
    times = []
    thing = ''
    txt = []
    txt2 = []
    formattedLoc = ''
    
    if len(place) > 0:
        formattedLoc = pat.sub('-', place)
        formattedLoc = pat2.sub('-', formattedLoc)
        # print(f'loc: {place} formattedLoc: {formattedLoc}')
        
        page = requests.get('https://www.tide-forecast.com/locations/' + formattedLoc + '/forecasts/latest/six_day')
        # print(f'page: {str(page.url)}')
        if pat3.search(page.url):
            tree = html.fromstring(page.content)
            times = tree.xpath('//tr[@class="tin sma"][2]')[0]  # Get nodes with times and heights
            txt = tree.xpath('//tr[@class="lar hea1"]')[0]  # Get nodes with the day/night indicator
            
            for thing in txt.xpath('td/span/text()'):  # Strip the list of unneeded text
                if thing not in ['ing', 'noon']:
                    # print(f'thing: {thing}')
                    txt2.append(thing)
            for count, aTime in enumerate(times.xpath("td")):
                # print(f'count = {count}  {txt2[count]}')
                if len(aTime.xpath("./div/b/text()")) > 0 and txt2[count] != 'night':
                    print(
                        f'Place: {place}   time: {aTime.xpath("div/b/text()")[0]}  height: {aTime.xpath("div/span/text()")[0]} ft')
        else:
            print(f'Unable to find location.')
            return (10)
    else:
        print(f'Unable to comply. Please check the location you are trying to find.')
        return (1)


def test_getidalInfo():
    assert getTidalInfo('New York, New York') is None
    assert getTidalInfo('') == 1


if __name__ == '__main__':
    print(f'Calling getTidal for New York, New York')
    getTidalInfo('New York, New York')


