# BaT Data Grabber
Bring A Trailer(BAT) is a popular online auction website for enthusiast cars. This traverse auction results and saves them as CSV

Bring A Trailer holds a trove of data on how certain models are performing. You can use this data to track trends over time. The goal of this project is to traverse the website of a given model and collect all sales history into a CSV file for later analysis.


## Schema
- URL: auction URL for the specific sale
- Title: contains vehicle information at a mininum make and model.
- Subtitle: Contains final price as well auction end date
- Model year
- Price
- Auction end date
- Sold
- Mileage
- Transmission
- Model Trim(only for Porshce 911 BaT model pages)

## Additional data cleaning may be required:
- parsing of model generation
- parsing of model trims

## Usage:
1. download python file
1. run the script with python 3.8 or greater
1. provide a BaT car model URL (ex: https://bringatrailer.com/porsche/911-gt3/ , https://bringatrailer.com/bmw/m3/?q=bmw%20m3)
1. script will launch browers and load all results
1. script will save all data in a file named BAT_data.csv




## Example Data analysis
- [Porsche GT3 Analysis](https://public.tableau.com/views/BaTGT3Market/BaTGT3Market?:language=en-US&:display_count=n&:origin=viz_share_link)
- [Porsche 997 BaT Analysis](https://public.tableau.com/views/997BaTAuctionResults/997BaTResults?:language=en-US&:display_count=n&:origin=viz_share_link)
- [BMW M5 BaT Analysis](https://public.tableau.com/views/BMWM5BaTAuctionResults/BmwM5BaTAnalysis?:language=en-US&:display_count=n&:origin=viz_share_link)
- [BMW M3 BaT Analysis](https://public.tableau.com/views/BMWM3BaTAuctionResults/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)
