import argparse
import ast
from ECBClient import ECBClientClass


if __name__ == '__main__':

    ecb_client = ECBClientClass()
    
    parser = argparse.ArgumentParser(description='Interface to retrieve economic data from official SDMX API of European Central Bank. Currently supports inflation index data (INX) and yield curve data (YC). When no period is defined, the maximum available data is retrieved.')
    
    group_inflation = parser.add_argument_group('Inflation Options')
    group_inflation.add_argument('-i', '--inflation', help='Retrieves inflation data. When no period is provided, it retrieves maximum available data history.', action='store_true')

    group_yield = parser.add_argument_group('Yield Options')
    group_yield.add_argument('-y', '--yield-curve', help='Retrieves yield curve data. When no period is provided, it retrieves maximum available data history. When neither --shortterm nor --longterm is given, it retrieves the 2Y10Y Par Yield.', action='store_true')
    group_yield.add_argument('-s', '--spread', help='Returns yield spread.', action='store_true')
    group_yield.add_argument('-st', '--shortterm', help='Define short-term par yield', choices=['3M', '6M', '9M', '1Y', '2Y'], default='2Y')
    group_yield.add_argument('-lt', '--longterm', help='Define long-term par yield', choices=['5Y','10Y', '15Y', '20Y', '30Y'], default='10Y')
    
    group_fx = parser.add_argument_group('Exchange Rate Options')
    group_fx.add_argument('-fx', '--exchange-rate', help='Retrieves exchange rate data. When no period is provided, it retrieves maximum available data history.', action='store_true')
    group_fx.add_argument('-c', '--currency', help='Define the currency for which exchange rate data should be retrieved', default='USD')


    parser.add_argument('-b', '--begin', type=str, help='Start date in YYYY-MM format. Can be used with each flag. When provided, --end must be defined as well.', default=None)
    parser.add_argument('-e', '--end', type=str, help='End date in YYYY-MM format. Can be used with each flag. When provided, --begin must be defined as well.', default=None)

    args = parser.parse_args()

    if args.inflation:
        ecb_client.get_inflation_data(args.begin, args.end)
    
    elif args.yield_curve:
        ecb_client.get_yield_data(args.spread, args.begin, args.end, args.shortterm, args.longterm)
    
    elif args.exchange_rate:
        ecb_client.get_exchange_rate_data(args.currency, args.begin, args.end)



    


