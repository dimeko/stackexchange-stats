from datetime import datetime
from json2html import json2html
import pandas as pd
from flatten_json import flatten
import json
import pkg_resources
import sys
from loguru import logger as log

def datetime_validation(date: str) -> bool:
    """**Validates date format**
    Args:
        date (str): A date string.

    Returns:
        bool: True if the given date format is `'%Y%m%d %H:%M:%S'`.
    
    Raises:
        ValueError: If the given date has not the correct format returns `False`.
    """
    try:
        datetime.strptime(date, '%Y%m%d %H:%M:%S')
    except ValueError:
        return False
    else:
        return True

def date_to_timestamp(date: str) -> int:
    """**Date to timestamp (UTC)**
    Args:
        date (str): A date string.

    Returns:
        int: The corresponding timestamp of the given date (milliseconds).
    
    Raises:
        ValueError: If the given date cannot be normalized.
    """
    try:
        normalized_date = int(round(datetime.strptime(date, '%Y%m%d %H:%M:%S').timestamp()))
    except ValueError:
        exit_app("Date format is not normalizable")
    else:
        return normalized_date
        
def format_output(input: dict, format: str):
    """**Date to timestamp (UTC)**
    Args:
        input (dict): Input key/value object.
        format (str): Output format. One of `json`, `csv`, `html`.

    Returns:
        any: One of `json`, `csv`, `html` (str). Defaults to `json`.
    """
    if format == "json":
        return json.dumps(input, indent=2)
    elif format == "csv":
        pd_obj = pd.read_json(json.dumps(flatten(input)), orient='index')
        csv_data = pd_obj.to_csv()
        return csv_data
    elif format == "html":
        return json2html.convert(json = input)
    else:
        return json.dumps(input, indent=2)
    
def logger(message: str, enabled: bool, type="info"):
    """**Log helper**
    Args:
        message (str): Logging message.
        enabled (bool): If True produce logs.
        type (str): Log type
    """
    if enabled:
        if type == "error":
            log.error(message)
        else:
            log.info(message)

def version():
    """**Version**
    """
    return pkg_resources.require("stats")[0].version

def exit_app(a=0):
    """**Exist**
    """
    sys.exit(a)