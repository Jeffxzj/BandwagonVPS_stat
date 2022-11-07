# BandwagonVPS_stat

Simple Python3 script to get Bandwagon VPS usage statistic using its API key.

## Requirement

* Python >= 3.6
* Python `requests` module

## Usage

Fill your BandwagonVPS API info to the .cfg file and run the script. It will output bandwidth usage in default.

```bash
python stat_bwg.py -c your_api_key.cfg
```

For other stat info, use the `-d`  option.  Check the `data_types.json` for different data types.

```bash
python stat_bwg.py -c your_api_key.cfg -d hostname
```
