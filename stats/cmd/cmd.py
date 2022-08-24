#!/usr/bin/env python3

import argparse
import sys
import os
from stats.core import core
from stats.core import utils
from stats.core import errors

def run():
    """**CLI entry point** <br />
    Calls the stats method and prints the final results. <br/>
    The interface is powered by `argparse` a core and simple Python module. <br/>
    Args:
        -s, --since (str): The start date
        -v, --version (): Show package version
        -u, --until (str): The end date
        -f, --ouput-format (str): The output format `json`, `csv`, `html`
        -l, --enable-logging (): If flag exists `loguru` will produce logs.
        -d, --development-ur; (str): Overrides the default Stackexchange's url.
        -c, --custom-filter (str): Overrides the default API filter.
        -m, --max-pages (int): Overrides the default max pages permitted count.

    Example:
    ```
    usage: stats [-h] -s SINCE -u UNTIL [-f OUTPUT_FORMAT] [-l]
             [-d DEVELOPMENT_URL] [-c CUSTOM_FILTER] [-m MAX_PAGES]

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show version
    -s SINCE, --since SINCE
                            start date
    -u UNTIL, --until UNTIL
                            end date
    -f OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                            output format
    -l, --enable-logging  enable logging
    -d DEVELOPMENT_URL, --development-url DEVELOPMENT_URL
                            development url
    -c CUSTOM_FILTER, --custom-filter CUSTOM_FILTER
                            custom filter
    -m MAX_PAGES, --max-pages MAX_PAGES
                            max page count
    ```
    """
    parser = argparse.ArgumentParser(prog='stats')
    parser.add_argument("-v", "--version", action='store_true', help="show version", required=False)
    parser.add_argument("-s", "--since", help="start date", type=str, required=False)
    parser.add_argument("-u","--until", help="end date", type=str, required=False)
    parser.add_argument("-f", "--output-format", help="output format", type=str, required=False)
    parser.add_argument("-l", "--enable-logging", action='store_true', help="enable logging", required=False)
    parser.add_argument("-d", "--development-url", help="development url", type=str, required=False)
    parser.add_argument("-c", "--custom-filter", help="custom filter", type=str, required=False)
    parser.add_argument("-m", "--max-pages", help="max page count", type=int, required=False)
    
    args = parser.parse_args()

    # Required
    since = args.since
    until = args.until
    
    # Not required
    format = args.output_format
    enable_logging = args.enable_logging
    development_url = args.development_url
    custom_filter = args.custom_filter
    max_pages = args.max_pages
    version = args.version
    
    # Could have changed the functionality here to look nicer
    if version == True and (since is None and until is None):
        print(f"version: v{utils.version()}")
        utils.exit_app()
    else:
        if since is None and until is None:
            parser.print_help()
            utils.exit_app(2)
        if since is None or until is None:
            parser.error("arguments -s, --since and -u --until are required")

    if utils.datetime_validation(since) and  utils.datetime_validation(until):
        try:
            result = core.stats(
                utils.date_to_timestamp(since), 
                utils.date_to_timestamp(until), 
                development_url, 
                custom_filter,
                max_pages,
                enable_logging
            )
        except errors.DangerousRemoteData as e:
            utils.exit_app(f"{e}")
        except KeyboardInterrupt:
            print('Interrupted')
            utils.exit_app()
        print(utils.format_output(result, format))
    else:
        sys.exit(f"Error: Invalid input data")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print('Interrupted')
       