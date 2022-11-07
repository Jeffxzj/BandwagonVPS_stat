import os
import sys
import json
import configparser
import argparse
import requests
from datetime import datetime

# some datatypes, to get more datatype check the data_types.json file
VPS_CONFIG = ['plan_disk', 'plan_ram', 'plan_swap']
BW_RELATED = ['plan_monthly_data', 'data_counter']


def read_cfg(path):
    cfgdict = {}
    try:
        if os.path.isfile(path) and os.access(path, os.R_OK):
            parser = configparser.RawConfigParser()
            if len(parser.read(path)) <= 0:
                sys.exit('no cfg file')
            try:
                cfgdict['req_addr'] = parser.get('info', 'req_addr')
                cfgdict['vps_api'] = parser.get('info', 'vps_api')
            except configparser.Error as e:
                sys.exit(e)

        else:
            sys.exit('not a regular file or can\'t read')
    except (OSError, TypeError) as e:
        sys.exit(e)
    return cfgdict


def byte_to_GB(bytes):
    return (bytes / 1024**3)


def req_vminfo(cfgdict, req_datatype):
    req_addr = cfgdict['req_addr'] + cfgdict['vps_api']
    try:
        response = requests.get(req_addr, timeout=5)
        response.raise_for_status()
    except Exception as err:
        sys.exit(f"Error occurred while posting request: {err}")  # Python 3.6
    
    data = response.json()[req_datatype]
    if req_datatype in BW_RELATED:
        data = byte_to_GB(data)
        if req_datatype == BW_RELATED[1]:
            total_bw = byte_to_GB(response.json()[BW_RELATED[0]])
            next_reset_day = response.json()['data_next_reset']
            dt_obj = datetime.fromtimestamp(next_reset_day)
            print("Bandwidth Usage: %.2f/%.2fGB " %(data, total_bw))
            print("Bandwidth will reset on", dt_obj)
    else: 
        print(data)
            
    '''
    Other datatypes may need different processing. It seems that  
    the bandwidth usage matters most to me.
    '''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, nargs=1, help="path of the api key config file")
    parser.add_argument("-d", "--data", type=str, nargs=1, help="requested data type of the VPS")

    args = parser.parse_args()

    if args.config != None:
        config_path = args.config[0]
    else:
        config_path = "your_api_key.cfg"

    cfgdict = read_cfg(config_path)
    
    with open("data_types.json", "r") as f:
        all_datatypes = json.loads(f.read()).keys()

    if args.data != None:
        if args.data[0] not in all_datatypes:
            sys.exit("expected data type not found")
        req_vminfo(cfgdict, args.data[0])
    else:
        req_vminfo(cfgdict, "data_counter") # request bandwidth usage in default