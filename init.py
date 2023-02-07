import argparse
from ECBClient import ECBClientClass
from BBKClient import BBKClientClass


if __name__ == '__main__':    
    
    parser = argparse.ArgumentParser(description='Interface to retrieve economic data from official SDMX API of European Central Bank and German Federal Bank.')
    
    group_inflation = parser.add_argument_group('INFLATION')
    group_inflation.add_argument('-i', '--inflation', help='Retrieves inflation data. When no period is provided, it retrieves maximum available data history.', action='store_true')

    group_yield = parser.add_argument_group('YIELD')
    group_yield.add_argument('-y', '--yield-curve', help='Retrieves yield curve data. When no period is provided, it retrieves maximum available data history. When neither --shortterm nor --longterm is given, it retrieves the 2Y10Y Spot Yield.', action='store_true')
    
    group_fx = parser.add_argument_group('EXCHANGE RATE')
    group_fx.add_argument('-fx', '--exchange-rate', help='Retrieves exchange rate data. When no period is provided, it retrieves maximum available data history.', action='store_true')
    group_fx.add_argument('-c', '--currency', help='Define the currency for which exchange rate data should be retrieved', default='USD')


    parser.add_argument('-b', '--begin', type=str, help='Start date in YYYY-MM format. Can be used with each flag. When provided, --end must be defined as well.', default='1980-01-01')
    parser.add_argument('-e', '--end', type=str, help='End date in YYYY-MM format. Can be used with each flag. When provided, --begin must be defined as well.', default='2099-12-31')
    parser.add_argument('-s', '--spread', help='Returns spread of long and short term series.', action='store_true')
    parser.add_argument('-st', '--shortterm', help="Define short-term period for time series. Works with --yield-curve and --euribor. (Yield: ['3M', '6M', '9M', '1Y', '2Y'], Euribor: ['1W', '1M', '3M', '6M', '9M', '12M']", default='3M')
    parser.add_argument('-lt', '--longterm', help="Define short-term period for time series. Works with --yield-curve and --euribor. (Yield: ['5Y','10Y', '15Y', '20Y', '30Y'], Euribor: ['1W', '1M', '3M', '6M', '9M', '12M'])", default='10Y')

    
    group_euribor = parser.add_argument_group('EURIBOR')
    group_euribor.add_argument('-eur', '--euribor', help='Retrieves Euribor data. When no period is provided, it retrieves maximum available data history.', action='store_true')
    
    group_eonia = parser.add_argument_group('EONIA')
    group_eonia.add_argument('-eon', '--eonia', help='Retrieves Eonia data. When no period is provided, it retrieves maximum available data history. This function takes EONIA history until last day (2021-12-31) and continues with up-to-date €STR data.', action='store_true')

    args = parser.parse_args()

    if args.inflation:
        ecb_client = ECBClientClass()
        ecb_client.get_inflation_data(args.begin, args.end)
    
    elif args.yield_curve:
        ecb_client = ECBClientClass()
        ecb_client.get_yield_data(args.spread, args.begin, args.end, args.shortterm, args.longterm)
    
    elif args.exchange_rate:
        ecb_client = ECBClientClass()
        ecb_client.get_exchange_rate_data(args.currency, args.begin, args.end)

    elif args.euribor:
        bbk_client = BBKClientClass()
        bbk_client.get_euribor_data(args.begin, args.end, args.shortterm, args.longterm, args.spread)

    elif args.eonia:
        bbk_client = BBKClientClass()
        bbk_client.get_eonia_data(args.begin, args.end)