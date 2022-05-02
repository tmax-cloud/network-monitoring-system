import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from library import *
from variable import *


def outTraffic():
    url = URL

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Out traffic "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".outtraffic",
                "value_type": 3, #numerinc unsigned
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.16."+interface[0], #out octect oid = 1.3.6.1.2.1.2.2.1.10.+index
                "units" : "bps",
                "delay" : "1m",
                "history" : "7d",
                "trends" : "0s",
                "tags" : [
                    {
                        "tag": "Interface",
                        "value" : interface[1]
                    },
                    {
                        "tag": "Interface Information",
                        "value" : "out traffic"
                    }
                ],
                "preprocessing": [ #change per second(Octet*8)
                    {
                        "type": "1",
                        "params": "8",
                        "error_handler": "1",
                        "error_handler_params": ""
                    },
                    {
                        "type": "10",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
        print(json.dumps(response, indent=3, sort_keys=True))

if __name__ == "__main__":
    outTraffic()
