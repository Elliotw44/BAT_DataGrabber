# BAT Data Grabber
Bring A Trailer(BAT) is a popular online auction website for enthusiast cars. This traverse auction results and saves them as CSV

Bring A Trailer holds a trove of data on how certain models are performing. You can use this data to all track trends over time. The goal of this project is to traverse the website of a given model and collect all sales history into a CSV file for later analysis. 


## Schema
- Url: auction URL for the specific sale
- Title: contains vehicle information at a mininum make and model.
- Subtitle: Contains final price as well auction end date
- Model year
- Price
- Auction end date
- Sold

## Some Additional data cleaning may be required:
- parsing of model generation
- parsing of model trims
- removing  non-vehicle item sales from results
- parsing of price and auction end date


## Usage:
1. download python file
1. run the script with python 3.8 or greater
1. provide a BaT car model URL (ex: https://bringatrailer.com/porsche/911-gt3/ , https://bringatrailer.com/bmw/m3/?q=bmw%20m3)
1. script will launch browers and load all results
1. script will save all data in a file named BAT_data.csv




## Example Data analysis
https://public.tableau.com/app/profile/elliotw/viz/BaTGT3Market/BaTGT3Market?publish=yes
