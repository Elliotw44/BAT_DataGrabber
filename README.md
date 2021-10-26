# BAT_DataGrabber
Bring A Trailer(BAT) is a popular online auction website for enthusiast cars. This traverse auction results and saves them as CSV


Bring A Trailer holds a trove of data on how certain models are performing. You can use this data to all track trends over time. The goal of this project is to traverse the website of a given model and collect all sales history into a CSV file for later analysis. 
The current schema is:
- Id: an internal Id most likely used by BaT
- Url: auction URL for the specific sale
- Title: contains vehicle information at a mininum make and model.
- Subtitle: Contains final price as well auction end date
- Images: a URl to a small image of the vehicle

Some Additional data cleaning may be required:
- parsing of model generation
- parsing of model trims
- removing  non-vehicle item sales from results
- parsing of price and auction end date



