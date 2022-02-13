# helsinki-apartment-finder

# A python framework for apartment finding in Helsinki

With this tool, you can scrape apartment information from [oikotie asunnot](https://asunnot.oikotie.fi/).

For changing the considered locations, modify the [locations_url](https://github.com/doruirimescu/helsinki-apartment-finder/blob/8efa101e6b135a926ac184956de5c76dbc4bdcc7/parameters.py#L24) parameter

The top candidate apartments can be plotted on a radar chart:
![Selection_103](https://user-images.githubusercontent.com/7363000/153774509-d248c7be-fc3c-4001-aeba-afc7c4fc1dc8.png)

The top candidate apartments are sorted based on their ranks:
![Selection_105](https://user-images.githubusercontent.com/7363000/153774865-5f4c42e4-cd12-469b-87cf-67b1444734ce.png)

**Before running:** 
* Install [chromedriver](https://chromedriver.chromium.org/downloads)
* Configure [parameters](https://github.com/doruirimescu/helsinki-apartment-finder/blob/master/parameters.py)

**Running:**
```python3 scraper.py```

Inspired from: https://github.com/jarvijaakko/Apartment_hunting
