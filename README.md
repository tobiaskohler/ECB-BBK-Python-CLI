# ECB Data Retrieval - Python CLI


This repository provides a command-line interface to retrieve economic data from [European Central Bank's (ECB) SDMX API](https://sdw-wsrest.ecb.europa.eu/help/).

## Features
- Retrieve inflation index data (INX) 
- Retrieve yield curve data (YC) 
- Retrieve exchange rate data (EXR)
- Define custom start and end dates for data retrieval 
- Option to calculate yield spread 
- Option to save output as .PNG, interactive .HTML and time series as .CSV

## Requirements / Installation
- Python 3.x
- argparse library
- ast library

To install the required packages, navigate to the root directory of the project and run the following command.

```
pip install -r requirements.txt
```


## Usage
To generate a plot of the inflation rate in the Eurozone with total available data:

```
> init.py [-h]

options:
  -h, --help            show this help message and exit
  -b BEGIN, --begin BEGIN
                        Start date in YYYY-MM format. Can be used with each flag. When provided, --end must be defined as well.
  -e END, --end END     End date in YYYY-MM format. Can be used with each flag. When provided, --begin must be defined as well.

INFLATION:
  -i, --inflation       Retrieves inflation data. When no period is provided, it retrieves maximum available data history.

YIELD:
  -y, --yield-curve     Retrieves yield curve data. When no period is provided, it retrieves maximum available data history. When neither --shortterm nor --longterm
                        is given, it retrieves the 2Y10Y Par Yield.
  -s, --spread          Returns yield spread.
  -st {3M,6M,9M,1Y,2Y}, --shortterm {3M,6M,9M,1Y,2Y}
                        Define short-term par yield
  -lt {5Y,10Y,15Y,20Y,30Y}, --longterm {5Y,10Y,15Y,20Y,30Y}
                        Define long-term par yield

EXCHANGE RATE:
  -fx, --exchange-rate  Retrieves exchange rate data. When no period is provided, it retrieves maximum available data history.
  -c CURRENCY, --currency CURRENCY
                        Define the currency for which exchange rate data should be retrieved
```

## Examples

### 1. Inflation data
Retrieve information about monthly inflation rate in Eurozone using maximum available data history:

```
> init .py -b 2015-01 -e 2022-12
```

 Outputs:

![Example 1](./HICP_Eurozone_2022-12-01-1998-01-01.png)

You always get prompted to save output: 

````
Save output to the current folder? (y/n)
````

`y` will save the static image as .PNG, the interactive HTML and the .CSV file to output/ folder.


### 2. Yield data
Retrieve information about daily (par) yield curve in Eurozone using data from 2005-01 to 2021-12:

```
> init.py -y -b 2005-01 -e 2021-12
```

Outputs:

![Example 2](Yield_curve_2Y10Y_2021-12-31-2005-01-03_spread-False.png)

### 3. Yield data (spread)
Retrieve information about daily (par) yield spread (6M5Y):

```
> init.py -y -s -st 6M -lt 5Y
```

Outputs

![Example 3](Yield_curve_6M5Y_2023-02-02-2004-09-06_spread-True.png)

### 4. Exchange rate data (FX)
Retrieve information about daily EUR/USD exchange rate with maximum available time series data:

```
> init.py -fx
```

Outputs:

![Example 4](./FX_USD_EUR_1999-01-04-2023-02-03.png)

### 5. Exchange rate data for e.g. GBP
Retrieve information about daily EUR/GBP exchange rate during January 2005 till December 2010:

```
> init.py -fx -c GBP -b 2005-01 -e 2010-12
```

Outputs:

![Example 4](./FX_GBP_EUR_2005-01-03-2010-12-31.png)

## Future implementations
- get GDP data


## Feedback & Contribution

If you have feedback, ideas for improving the project or found a bug , please open an issue.
