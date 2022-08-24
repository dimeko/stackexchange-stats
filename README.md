# Stats
This is a simple CLI tool that calculates StackOverflow answers and comments statictics
for a given time period.

## Installation
With **Makefile**:
```
make install # For production-like installation
```
```
make install-dev # For dev installation
```

Or:
```
python3 -m pip install . # For production-like installation
```
```
python3 -m pip install -e .'[dev]' # For dev installation
```
**NOTE**: the `'[dev]'` instead of `[dev]` is for running the command is for `zsh` users only since `zsh` parses `[dev]` as a string match. If you use `bash` use `[dev]` instead.

## Usage
After installation an executable will be available with that name `stats`.
Usage:
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
#### Required:
- `--since` and `--until` input arguments must be of format `'%Y%m%d %H:%M:%S'` example: "20220807 10:00:00"

#### Not required:
- `--output-format` must be one of `json`, `csv` or `html`. It default to `json`.
- `--enable-logs` is just a flag. If exists, the application will produce logs.
- `--development-url` overrides the default Stackexchange's url.
- `--custom-filter` overrides the default API filter.
- `--max-pages` overrides the default max pages permitted count.

## Tests
With **Makefile**:
```
make tests
```
Or:
```
python3 -m pip install -e .'[dev]' # If you do not have already installed it
python3 -m pytest -vv
```
## Documentation
With **Makefile**:
```
make docs
```
Or:
```
python3 -m pip install .'[dev]' # If you do not have already installed it
python3 -m mkdocs serve
```
